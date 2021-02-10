import datetime
import app.services.serialization as json


class ApiResponse:
    def getMessage(self, method):
        switcher = {
            'post-success': 'Insert Success',
            'put-success': 'Update Success',
            'delete-success': 'Update Success',

            'post-failed': 'Insert Failed',
            'put-failed': 'Update Failed',
            'delete-failed': 'Delete Failed',

            'data-failed': 'Missing Parameters',
            'authentication-failed': 'Invalid Auth Token',

            'permission-failed': 'Permission Denied',
            'notfound-failed': 'Page Not Found',
            'error-failed': 'Internal Error',
            'server-failed': 'Internal Server Error'
        }

        return switcher.get(method, method)


    def success(self, param, data = '', pagination = None, startTime = None):
        resData = {
            'status': 'success',
            'message': self.getMessage(param+'-success'),
            'executionTime': (datetime.datetime.now() - startTime).microseconds / 100000 if startTime is not None else 0,
            'data': data
        }

        if pagination is not None:
            resData['pagination'] = pagination

        return resData
        # return json.dumps(resData)


    def failed(self, param, data = ''):
        resData = {
            'status': 'failed',
            'message': self.getMessage(param+'-failed'),
            'executionTime': 0,
            'data': data
        }

        return resData
        # return json.dumps(resData)
