import falcon
import datetime
import logging

import app.services.serialization as json

from app.services.apiResponse import ApiResponse
from app.services.apiError import ApiError


class TokenValidation(object):
    def __init__(self, config):
        self.apiResponse = ApiResponse()
        self.config = config

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            return

        request_token = req.get_header(self.config.SECRET_KEY)
        
        if request_token is None or request_token != self.config.SECRET_KEY_HASH:
            raise ApiError(falcon.HTTP_401, self.apiResponse.failed('authentication', ''))


class JSONTranslator(object):
    def __init__(self, config):
        self.apiResponse = ApiResponse()
        self.config = config

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            return

        req.context['startTime'] = datetime.datetime.now()
        req.context['status'] = 'status'

        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise ApiError(falcon.HTTP_400, self.apiResponse.failed('json', ''))
        try:
            req.context['data'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise ApiError(falcon.HTTP_400, self.apiResponse.failed('error', ''))

    def process_response(self, req, resp, resource):
        if req.method == 'OPTIONS':
            return
        
        if 'result' in req.context:
            resp.status = falcon.HTTP_200
            resp.body = self.apiResponse.success(req.context['status'], req.context['result'], req.context['pagination'] if 'pagination' in req.context else None, req.context['startTime'])
            return

        if 'error' in req.context:
            resp.status = req.context['statusCode'] if 'statusCode' in req.context else falcon.HTTP_200
            resp.body = self.apiResponse.failed(req.context['status'], req.context['error'], req.context['startTime'])
            return
        
        resp.status = falcon.HTTP_404
        resp.body = self.apiResponse.failed('notfound', '')
        
