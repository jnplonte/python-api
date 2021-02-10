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

from app.models.routings import Routings


class AppReportLoadPlan(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.customer = g.customer

        self.api_response = api_response

        self.routings = Routings(mongo_connection, False)

        self.parser = reqparse.RequestParser()

        self.startTime = datetime.now()

        self.isTest = False


    def get(self):
        return notFound(self.api_response.failed)


    def put(self):
        return notFound(self.api_response.failed)


    """
    @api {post} /report/loadplan load plan report
    @apiVersion 1.0.0
    @apiName loadplan
    @apiGroup REPORT
    @apiPermission all
    @apiDescription generate load plan report
    
    @apiParam (query) {String} [type=data] report type <br/> sample: `data|xls|pdf`
    @apiParam (body) {Array} code routing codes
    @apiParam (body) {Array} [truckId] truck id, if given this will filter out the trucks that has the truck id
    @apiParam (body) {Array} [planId] plan id, if given this will filter out the trucks that has the plan id
    @apiParam (body) {Array} [projectCode] project code, if given this will filter out the trucks that has the project code
    @apiParam (body) {Array} [blockProjectCode] blocked project code, if given this will ignore out the trucks that has blocked project code
    """
    def post(self):
        self.parser.add_argument('type', type=str, default='data')
        self.parser.add_argument('code', type=list, location='json')
        self.parser.add_argument('truckId', type=list, location='json')
        self.parser.add_argument('planId', type=list, location='json')
        self.parser.add_argument('projectCode', type=list, location='json')
        self.parser.add_argument('blockProjectCode', type=list, location='json')

        self.parser.add_argument('test', type=str, location='args')
        
        data = self.parser.parse_args()

        self.isTest = (data['test'] is not None and data['test'] == 'true')

        if self.checkRequiredParameters(data) is False:
            return self.api_response.failed('data', ['code'])

        if self.isTest:
            reportName = 'test.xlsx'
        else:
            reportName = self.customer['code'] + '/' + datetime.today().strftime('%Y-%m-%d') + '-' + random(8) + '.xlsx'
        
        reportType = data['type'] if data['type'] is not None else 'data'

        try:
            queryData = self.getFinalData(data)
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
        if data['code'] is None:
            return False
        
        return True

    def getFinalData(self, data):
        findQueryData = []

        queryData = self.getData(data['code'], data['planId'], data['truckId'])
        if len(queryData) >= 1:
            if data['projectCode'] is not None and len(data['projectCode']) >= 1 and len(findQueryData) == 0:
                for qindx, qdata in enumerate(queryData):
                    if 'data' in qdata and len(qdata['data']) >= 1:
                        for dindx, ddata in enumerate(qdata['data']):
                            if 'routes' in ddata and len(ddata['routes']) >= 1:
                                newOrder = []
                                for pcindx, pcdata in enumerate(ddata['routes']):
                                    if 'projectCode' in pcdata and len(pcdata['projectCode']) >= 1 and any(elem in data['projectCode']  for elem in pcdata['projectCode']):
                                        newOrder.append(pcdata)
                                ddata['routes'] = newOrder

                        findQueryData.append(qdata)


            if data['truckId'] is not None and len(data['truckId']) >= 1 and len(findQueryData) == 0:
                for qindx, qdata in enumerate(queryData):
                    if 'data' in qdata and len(qdata['data']) >= 1 and 'truckId' in qdata and any(elem in data['truckId']  for elem in qdata['truckId']):
                        findQueryData.append(qdata)


            if data['planId'] is not None and len(data['planId']) >= 1 and len(findQueryData) == 0:
                for qindx, qdata in enumerate(queryData):
                    if 'data' in qdata and len(qdata['data']) >= 1 and 'planId' in qdata and any(elem in data['planId']  for elem in qdata['planId']):
                        findQueryData.append(qdata)


            if len(findQueryData) == 0:
                findQueryData = queryData

        # filter block project codes
        if data['blockProjectCode'] is not None and len(data['blockProjectCode']) >= 1:
            finalData = []
            for findx, fdata in enumerate(findQueryData):
                if 'data' in fdata and len(fdata['data']) >= 1:
                    for fdindx, fddata in enumerate(fdata['data']):
                        if 'routes' in fddata and len(fddata['routes']) >= 1:
                            newOrder = []
                            for fpcindx, fpcdata in enumerate(fddata['routes']):
                                if 'projectCode' in fpcdata and len(fpcdata['projectCode']) >= 1 and any(elem not in data['blockProjectCode']  for elem in fpcdata['projectCode']):
                                    newOrder.append(fpcdata)
                            fddata['routes'] = newOrder

                    finalData.append(fdata)

            return finalData
        # filter block project codes

        return findQueryData

    def updateJson(self, data):
        if len(data) == 0:
            return []

        finalData = []
        for qindx, qdata in enumerate(data):
            if 'data' in qdata and len(qdata['data']) >= 1:
                for vindx, vdata in enumerate(qdata['data']):
                    vehicleData = vdata

                    vehicleData['code'] = qdata['code'] if 'code' in qdata else ''

                    finalData.append(vehicleData)

        if len(finalData) == 0:
            return []

        waypointData = []
        orderData = []

        finalRoutes = []
        for findx, fdata in enumerate(finalData):
            if 'routes' in fdata and len(fdata['routes']) >= 1:
                for rindx, rdata in enumerate(fdata['routes']):
                    routeData = rdata

                    routeData['code'] = fdata['code'] if 'code' in fdata else ''
                    routeData['plateNumber'] = fdata['plateNumber'] if 'plateNumber' in fdata else ''
                    routeData['truckId'] = fdata['truckId'] if 'truckId' in fdata else ''

                    if 'waypointId' in routeData and len(routeData['waypointId']) >= 1:
                        waypointData = waypointData + routeData['waypointId']

                    if 'orderId' in routeData and len(routeData['orderId']) >= 1:
                        orderData = orderData + routeData['orderId']

                    finalRoutes.append(routeData)

        if len(finalRoutes) == 0:
            return []

        fFinalRoute = groupBy(finalRoutes, 'planId')
        fFinalRoutes = []
        for finalIndex, finalRoute in fFinalRoute.items():
            fFinalRoutes.append({
                'code': finalRoute[0]['code'] if finalRoute[0] is not None and 'code' in finalRoute[0] else '',
                'planId': finalIndex,
                'plateNumber': finalRoute[0]['plateNumber'] if finalRoute[0] is not None and 'plateNumber' in finalRoute[0] else '',
                'truckId': finalRoute[0]['truckId'] if finalRoute[0] is not None and 'truckId' in finalRoute[0] else '',

                'waypoints': list(dict.fromkeys(waypointData)),
                'orders': list(dict.fromkeys(orderData)),
                'routes': finalRoute
            })

        return fFinalRoutes

    def getData(self, code, planId, truckId):
        query = {'customerId': self.customer['_id']}

        if code is not None:
            query['code'] = {'$in': code}

        if planId is not None:
            query['planId'] = {'$in': planId}

        if truckId is not None:
            query['truckId'] = {'$in': truckId}
              
        return self.routings.getAllFields(query)

    def generateXls(self, queryData, reportName):

        if self.isTest:
            workbook = xlsxwriter.Workbook(reportName)
        else:
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)

        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        for indx, data in enumerate(queryData):
            worksheet.write(row, 0, 'CODE:')
            worksheet.write(row, 1, data['code'])
            row += 1

            worksheet.write(row, 0, 'PLAN ID:')
            worksheet.write(row, 1, data['planId'] if 'planId' in data and data['planId'] is not None else '')
            row += 1
            worksheet.write(row, 0, 'PLATE NO:')
            worksheet.write(row, 1, data['plateNumber'] if 'plateNumber' in data and data['plateNumber'] is not None else '')
            row += 1
            worksheet.write(row, 0, 'ROUTES:')
            row += 1
            worksheet.write(row, col, 'NO')
            worksheet.write(row, col + 1, 'ZONE')
            worksheet.write(row, col + 2, 'PLAN ID')
            worksheet.write(row, col + 3, 'PROJECT CODE')
            worksheet.write(row, col + 4, 'CUSTOMER CODE')
            worksheet.write(row, col + 5, 'SHIPMENT REFERENCE')
            worksheet.write(row, col + 6, 'ADDRESS')
            worksheet.write(row, col + 7, 'WEIGHT')
            worksheet.write(row, col + 8, 'CMB')
            worksheet.write(row, col + 9, 'START TIME')
            worksheet.write(row, col + 10, 'END TIME')
            row += 1
            if 'routes' in data and len(data['routes']) >= 1:
                startCount = row + 1
                for rindx, rdata in enumerate(data['routes']):
                    worksheet.write(row, col, rindx + 1)
                    worksheet.write(row, col + 1, rdata['zone'] if 'zone' in rdata and rdata['zone'] is not None else '')
                    worksheet.write(row, col + 2, rdata['planId'] if 'planId' in rdata and rdata['planId'] is not None else '')
                    worksheet.write(row, col + 3, ', '.join(rdata['projectCode']) if 'projectCode' in rdata and rdata['projectCode'] is not None else '')
                    worksheet.write(row, col + 4, ', '.join(rdata['customerCode']) if 'customerCode' in rdata and rdata['customerCode'] is not None else '')
                    worksheet.write(row, col + 5, ', '.join(rdata['shipmentReference']) if 'shipmentReference' in rdata and rdata['shipmentReference'] is not None else '')
                    worksheet.write(row, col + 6, rdata['displayAddress'] if 'displayAddress' in rdata and rdata['displayAddress'] is not None else '')
                    worksheet.write(row, col + 7, rdata['capacity1'] if 'capacity1' in rdata and rdata['capacity1'] is not None else 0)
                    worksheet.write(row, col + 8, rdata['capacity2'] if 'capacity2' in rdata and rdata['capacity2'] is not None else 0)
                    worksheet.write(row, col + 9, rdata['startTime'] if 'startTime' in rdata and rdata['startTime'] is not None else '')
                    worksheet.write(row, col + 10, rdata['endTime'] if 'endTime' in rdata and rdata['endTime'] is not None else '')
                    row += 1
                endCount = row
            
                row += 1
                worksheet.write(row, 0, 'TOTAL ORDER:')
                worksheet.write(row, 1, len(data['routes']))
                row += 1
                worksheet.write(row, 0, 'TOTAL WEIGHT:')
                worksheet.write(row, 1, '=SUM(H' + str(startCount) + ':H' + str(endCount) + ')')
                row += 1
                worksheet.write(row, 0, 'TOTAL CBM:')
                worksheet.write(row, 1, '=SUM(I' + str(startCount) + ':I' + str(endCount) + ')')
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


def startReportLoadPlan(api, config, api_response, mongo_connection):
    api.add_resource(AppReportLoadPlan, '/v1/report/loadplan', endpoint = 'loadplan', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
