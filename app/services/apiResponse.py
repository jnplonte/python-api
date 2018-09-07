import datetime
import app.services.serialization as json

class ApiResponse:

    def getMessage(self, method):
        switcher = {
            'post-success': 'Insert Success',
            'post-failed': 'Insert Failed',
            'data-failed': 'Missing Parameters',
            'data-success': 'Missing Parameters',
            'permission-failed': 'Permission Denied',
            'database-failed': 'Database Error',
            'notfound-failed': 'Page Not Found',
            'error-failed': 'Internal Server Error',
            'json-error': 'Invalid JSON Data',
            'generate-success': 'Generation Success',
            'generate-failed': 'Generation Failed',
            'authentication-failed': 'Invalid auth token'
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

        return json.dumps(resData)

    def failed(self, param, data = '', startTime = None):
        resData = {
            'status': 'failed',
            'message': self.getMessage(param+'-failed'),
            'executionTime': (datetime.datetime.now() - startTime).microseconds / 100000 if startTime is not None else 0,
            'data': data
        }

        return json.dumps(resData)
