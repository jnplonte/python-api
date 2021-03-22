from datetime import datetime

from flask_restful import Resource, reqparse

from app.services.query import query
from app.services.not_found import notFound

from app.models.users import Users

class CoreUser(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.startTime = datetime.now()

        self.api_response = api_response

        self.users = Users(mongo_connection, False)

        self.parser = reqparse.RequestParser()


    """
    @api {get} /core/user/:id get one user
    @apiVersion 1.0.0
    @apiName get
    @apiGroup USERS
    @apiPermission authenticated-user
    @apiDescription get one users
    
    @apiParam (url segment) {String} id user id
    @apiParam (url parameter) {String} key key search Ex. ?key=name
    """
    def get(self, id=None):
        self.parser.add_argument('key', type=str, location='args', default='_id')

        data = self.parser.parse_args()

        try:
            queryData = self.getOneData(data['key'], id)
            if not bool(queryData):
                return self.api_response.failed('get', '')
    
            return self.api_response.success('get', queryData, startTime=self.startTime)
        except Exception as e:
            return self.api_response.failed('get', str(e))


    def post(self, id=None):
        return notFound(self.api_response.failed)


    def put(self, id=None):
        return notFound(self.api_response.failed)


    def delete(self, id=None):
        return notFound(self.api_response.failed)

# ---------------------------------------------------------------------------------------------------------------------

    def getOneData(self, key, kId):
        if key == '_id':
            return self.users.getById(kId)
        else:
            return self.users.get({key: kId})

# ---------------------------------------------------------------------------------------------------------------------

def startUser(api, config, api_response, mongo_connection):
    api.add_resource(CoreUser, '/v1/core/user/<string:id>', endpoint = 'user', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
