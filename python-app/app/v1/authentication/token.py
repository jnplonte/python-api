import copy
import uuid

from datetime import datetime
from bson.objectid import ObjectId

from flask import g
from flask_restful import Resource, reqparse


from app.services.query import query
from app.services.not_found import notFound

class Token(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.user = g.user

        self.api_response = api_response

        self.parser = reqparse.RequestParser()

        self.startTime = datetime.now()


    def get(self):
        return notFound(self.api_response.failed)


    """
    @api {post} /custom/updategpsdata update order planning gps data
    @apiVersion 1.0.0
    @apiName post-gpsdata
    @apiGroup CUSTOM
    @apiPermission all
    @apiDescription update order planning gps data

    @apiParam (body) {String} deviceId device id
    @apiParam (body) {String} posAt position 
    @apiParam (body) {String} latLongG lat-lng google
    @apiParam (body) {String} latLongB lat-lng baidu
    @apiParam (body) {String} latLongA lat-lng amap
    @apiParam (body) {String} battery battery
    @apiParam (body) {String} addCode address code (routeData.companyName)
    @apiParam (body) {String} distance distance
    @apiParam (body) {String} lockStatus lock status

    @apiParam (body) {String} [user] user name
    @apiParam (body) {String} [emailAlert] email alert
    """
    def post(self):
        return self.api_response.success('token', 'xxxx', startTime=self.startTime)


    def put(self):
        return notFound(self.api_response.failed)


    def delete(self):
        return notFound(self.api_response.failed)

# ---------------------------------------------------------------------------------------------------------------------

    def checkRequiredPostParameters(self, data):
        if data['email'] is None:
            return False
        
        return True

# ---------------------------------------------------------------------------------------------------------------------

def startToken(api, config, api_response, mongo_connection):
    api.add_resource(Token, '/auth/token', endpoint = 'token', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
