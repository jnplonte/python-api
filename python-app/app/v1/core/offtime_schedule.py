import xlsxwriter
import oss2

from io import BytesIO
from datetime import datetime

from flask import g
from flask_restful import Resource, reqparse

from app.services.random import random
from app.services.query import query
from app.services.not_found import notFound
from app.services.group_by import groupBy

from app.models.schedules import ScheduleRoutings


class AppReportOfftimeSchedule(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.customer = g.customer

        self.api_response = api_response

        self.routings = ScheduleRoutings(mongo_connection, False)

        self.parser = reqparse.RequestParser()

        self.startTime = datetime.now()

        self.isTest = False


    def get(self):
        return notFound(self.api_response.failed)


    def put(self):
        return notFound(self.api_response.failed)


    """
    @api {post} /report/offtimeschedule offtime schedule report
    @apiVersion 1.0.0
    @apiName offtimeschedule
    @apiGroup REPORT
    @apiPermission all
    @apiDescription generate offtime schedule report
    
    @apiParam (query) {String} [type=data] report type <br/> sample: `data|xls|pdf`
    @apiParam (body) {String} startDate start date
    @apiParam (body) {String} endDate end date
    @apiParam (body) {Array} [projectCode] project code, if given this will filter out the trucks that has the project code
    @apiParam (body) {Array} [blockProjectCode] blocked project code, if given this will ignore out the trucks that has blocked project code
    """
    def post(self):
        self.parser.add_argument('type', type=str, default='data')
        self.parser.add_argument('startDate', type=str)
        self.parser.add_argument('endDate', type=str)
        self.parser.add_argument('projectCode', type=list, location='json')
        self.parser.add_argument('blockProjectCode', type=list, location='json')

        self.parser.add_argument('test', type=str, location='args')
        
        data = self.parser.parse_args()

        self.isTest = (data['test'] is not None and data['test'] == 'true')

        if self.checkRequiredParameters(data) is False:
            return self.api_response.failed('data', ['startDate', 'endDate'])

        if self.isTest:
            reportName = 'test.xlsx'
        else:
            reportName = self.customer['code'] + '/' + datetime.today().strftime('%Y-%m-%d') + '-' + random(8) + '.xlsx'
        
        reportType = data['type'] if data['type'] is not None else 'data'

        try:
            startTime = str(datetime.now().strftime('%Y-%m-%d')) + ' 00:00:00' if data['startDate'] is None else str(datetime.strptime(data['startDate'],'%Y-%m-%d'))
            endTime = str(datetime.now().strftime('%Y-%m-%d')) + ' 23:59:59' if data['endDate'] is None else str(datetime.strptime(data['endDate'],'%Y-%m-%d')).replace('00:00:00', '23:59:59')

            queryData = self.getData(startTime, endTime, data['projectCode'])

            if len(queryData) == 0:
                return self.api_response.success('raw-data', [], startTime=self.startTime)

            finalData = self.updateJson(queryData)
            if reportType == 'data':
                return self.api_response.success('raw-data', finalData, startTime=self.startTime)

            if reportType == 'xls':
                if len(finalData) >= 1:
                    xlsData = self.generateXls(finalData, reportName)
                    if self.isTest:
                        return self.api_response.success('raw-data', 'test', startTime=self.startTime)
                    else:
                        try:
                            bucketInfo = self.storeAlibabaOss(reportName, xlsData)

                            return self.api_response.success('xls-report', 'https://' + bucketInfo.name + '.' + bucketInfo.extranet_endpoint + '/' + reportName, startTime=self.startTime)
                        except oss2.exceptions.NoSuchKey as e:
                            return self.api_response.failed('xls-report', str(e))
                else:
                    return self.api_response.failed('xls-report', 'no data')

            if reportType == 'pdf':
                return self.api_response.success('pdf-report', finalData, startTime=self.startTime)

            return self.api_response.success('raw-data', finalData, startTime=self.startTime)

        except Exception as e:
            return self.api_response.failed('raw-data', str(e))


    def delete(self):
        return notFound(self.api_response.failed)

    # ---------------------------------------------------------------------------------------------------------------------

    def checkRequiredParameters(self, data):
        if data['startDate'] is None or data['endDate'] is None:
            return False
        
        return True

    def getData(self, startTime, endTime, projectCode):
        query = {'customerId': self.customer['_id']}
        if startTime is not None and endTime is not None:
            query['startTime'] = {'$gte': startTime, '$lte': endTime}
            query['endTime'] = {'$gte': startTime, '$lte': endTime}

        if projectCode is not None and len(projectCode) >= 1:
            query['projectCode'] = {'$in': projectCode}

        return self.routings.getAllFields(query)

    def updateJson(self, data):
        if len(data) == 0:
            return []

        finalData = []
        for dIndx, dData in enumerate(data):
            if 'actualData' in dData and bool(dData['actualData']) and 'estimateOnTime' in dData['actualData'] and 'endOnTime' in dData['actualData']:
                if 'estimateOnTime' in dData['actualData'] and 'endOnTime' in dData['actualData']:
                    if dData['actualData']['estimateOnTime'] is False or dData['actualData']['endOnTime'] is False:
                        finalData.append({
                            '_id': dData['_id'],
                            'waypointType': dData['waypointType'],
                            'latitude': dData['latitude'],
                            'longitude': dData['longitude'],
                            'district': dData['district'],
                            'displayAddress': dData['displayAddress'],
                            'zone': dData['zone'],
                            'truckId': dData['truckId'],
                            'plateNumber': dData['plateNumber'],
                            'driverId': dData['driverId'],
                            'estimateTime': dData['estimateTime'],
                            'endTime': dData['endTime'],
                            'status': dData['status'],
                            'projectCode': dData['projectCode'][0] if len(dData['projectCode']) >= 1 else '',
                            'cycle': dData['additionalData']['cycle'] if 'cycle' in dData['additionalData'] else '',
                            'actualData': dData['actualData']
                        })

        if len(finalData) == 0:
            return []

        fFinalRoute = groupBy(finalData, 'truckId')

        fFinalRoutes = []
        for finalIndex, finalRoute in fFinalRoute.items():
            routesData = []
            for fIndx, fRoute in enumerate(finalRoute):
                routesData.append(fRoute)

            fFinalRoutes.append({
                'truckId': finalRoute[0]['truckId'] if finalRoute[0] is not None and 'truckId' in finalRoute[0] else '',
                'plateNumber': finalRoute[0]['plateNumber'] if finalRoute[0] is not None and 'plateNumber' in finalRoute[0] else '',

                'routes': routesData
            })

        return fFinalRoutes


    def generateXls(self, queryData, reportName):

        if self.isTest:
            workbook = xlsxwriter.Workbook(reportName)
        else:
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)

        worksheet = workbook.add_worksheet()

        cellFormatRed = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        cellFormatYellow = workbook.add_format({'bg_color': '#ffff7f', 'font_color': '#999900'})

        row = 0
        col = 0
        for indx, data in enumerate(queryData):
            worksheet.write(row, 0, 'PLATE NO:')
            worksheet.write(row, 1, data['plateNumber'] if 'plateNumber' in data and data['plateNumber'] is not None else '')
            row += 1
            worksheet.write(row, 0, 'ROUTES:')
            row += 1
            worksheet.write(row, col, 'NO')
            worksheet.write(row, col + 1, 'ROUTE')
            worksheet.write(row, col + 2, 'CYCLE')
            worksheet.write(row, col + 3, 'DRIVER')
            worksheet.write(row, col + 4, 'WAYPOINT')
            worksheet.write(row, col + 5, 'TYPE')

            worksheet.write(row, col + 6, 'ARRIVAL (EXPECTED)')
            worksheet.write(row, col + 7, 'ARRIVAL (ACTUAL)')
            worksheet.write(row, col + 8, 'ARRIVAL (DELAY TIME)')
            worksheet.write(row, col + 9, 'ARRIVAL (REASON)')

            worksheet.write(row, col + 10, 'DEPARTURE (EXPECTED)')
            worksheet.write(row, col + 11, 'DEPARTURE (ACTUAL)')
            worksheet.write(row, col + 12, 'DEPARTURE (DELAY TIME)')
            worksheet.write(row, col + 13, 'DEPARTURE (REASON)')
            row += 1
            if 'routes' in data and len(data['routes']) >= 1:
                startCount = row + 1
                for rindx, rdata in enumerate(data['routes']):
                    worksheet.write(row, col, rindx + 1)
                    worksheet.write(row, col + 1, rdata['projectCode'] if 'projectCode' in rdata and rdata['projectCode'] is not None else '')
                    worksheet.write(row, col + 2, rdata['cycle'] if 'cycle' in rdata and rdata['cycle'] is not None else 1)
                    worksheet.write(row, col + 3, '')
                    worksheet.write(row, col + 4, rdata['district'] if 'district' in rdata and rdata['district'] is not None else '')
                    worksheet.write(row, col + 5, self.getWaypointType(rdata['waypointType']) if 'waypointType' in rdata and rdata['waypointType'] is not None else '')

                    worksheet.write(row, col + 6, rdata['estimateTime'] if 'estimateTime' in rdata and rdata['estimateTime'] is not None else '')
                    worksheet.write(row, col + 7, rdata['actualData']['estimateTime'] if 'estimateTime' in rdata['actualData'] and rdata['actualData']['estimateTime'] is not None else '', self.checkColor(rdata['actualData'], 'estimate', cellFormatRed, cellFormatYellow))
                    worksheet.write(row, col + 8, int(rdata['actualData']['runningTimeDifference']) // 60 if rdata['actualData']['estimateOnTime'] is False and 'runningTimeDifference' in rdata['actualData'] else 0, self.checkColor(rdata['actualData'], 'estimate', cellFormatRed, cellFormatYellow))
                    worksheet.write(row, col + 9, rdata['actualData']['estimateReason'] if rdata['actualData']['estimateOnTime'] is False and 'estimateReason' in rdata['actualData'] else '', self.checkColor(rdata['actualData'], 'estimate', cellFormatRed, cellFormatYellow))

                    worksheet.write(row, col + 10, rdata['endTime'] if 'endTime' in rdata and rdata['endTime'] is not None else '')
                    worksheet.write(row, col + 11, rdata['actualData']['endTime'] if 'endTime' in rdata['actualData'] and rdata['actualData']['endTime'] is not None else '', self.checkColor(rdata['actualData'], 'end', cellFormatRed, cellFormatYellow))
                    worksheet.write(row, col + 12, int(rdata['actualData']['endRunningTimeDifference']) // 60 if rdata['actualData']['endOnTime'] is False and 'endRunningTimeDifference' in rdata['actualData'] else 0, self.checkColor(rdata['actualData'], 'end', cellFormatRed, cellFormatYellow))
                    worksheet.write(row, col + 13, rdata['actualData']['endReason'] if rdata['actualData']['endOnTime'] is False and 'endReason' in rdata['actualData'] else '', self.checkColor(rdata['actualData'], 'end', cellFormatRed, cellFormatYellow))
                    row += 1
                endCount = row
            
                row += 1
                worksheet.write(row, 0, 'TOTAL ORDER:')
                worksheet.write( row, 1, len(data['routes']) )
                row += 1
                worksheet.write(row, 0, 'TOTAL DELAY ARRIVAL:')
                worksheet.write( row, 1, '=SUM(I' + str(startCount) + ':I' + str(endCount) + ')' )
                row += 1
                worksheet.write(row, 0, 'TOTAL ORDER DEPARTURE:')
                worksheet.write( row, 1, '=SUM(M' + str(startCount) + ':M' + str(endCount) + ')' )
                row += 1
                worksheet.write(row, 0, 'TOTAL DELAY:')
                worksheet.write( row, 1, '=SUM(I' + str(startCount) + ':I' + str(endCount) + ',M' + str(startCount) + ':M' + str(endCount) + ')' )
                row += 2
            else:
                row += 3

        workbook.close()

        if self.isTest:
            return ''
        else:
            return output.getvalue()

    def storeAlibabaOss(self, reportName, xlsData):
        auth = oss2.Auth(self.config.OSS_KEY_ID, self.config.OSS_KEY_SECRET)
        bucket = oss2.Bucket(auth, self.config.OSS_DOMAIN, self.config.OSS_BUCKET)
        
        bucket.put_object(reportName, xlsData)

        return bucket.get_bucket_info()

    def getWaypointType(self, wpType):
        switcher = {
            't': 'ACTION',
            'T': 'ACTION',
            'p': 'PICKUP',
            'P': 'PICKUP',
            'd': 'DROPOFF',
            'D': 'DROPOFF'
        }

        return switcher.get(wpType, 'PICKUP')

    def checkColor(self, actualData, aType, red, yellow):
        if aType == 'estimate' and actualData['estimateOnTime'] is False and 'runningTimeDifference' in actualData:
            if int(actualData['runningTimeDifference']) >= 1800:
                return red
            else:
                return yellow

        if aType == 'end' and actualData['endOnTime'] is False and 'endRunningTimeDifference' in actualData:
            if int(actualData['endRunningTimeDifference']) >= 1800:
                return red
            else:
                return yellow

        return None


def startReportOfftimeSchedule(api, config, api_response, mongo_connection):
    api.add_resource(AppReportOfftimeSchedule, '/v1/report/offtimeschedule', endpoint = 'offtimeschedule', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
