from datetime import datetime

from flask_restful import Resource, reqparse

from app.services.query import query
from app.services.not_found import notFound

from app.models.users import Users

class CoreUsers(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.startTime = datetime.now()

        self.api_response = api_response

        self.users = Users(mongo_connection, False)

        self.parser = reqparse.RequestParser()


    """
    @api {get} /core/users get all users
    @apiVersion 1.0.0
    @apiName getAll
    @apiGroup USERS
    @apiPermission authenticated-user
    @apiDescription get all users
    
    @apiParam (query) {String} [query] query <br/> sample: `?query=test:abc`
    @apiParam (query) {Number} [page] page 
    @apiParam (query) {Number} [limit] limit
    """
    def get(self):
        self.parser.add_argument('query', type=str, location='args')
        self.parser.add_argument('page', type=int, location='args')
        self.parser.add_argument('limit', type=int, location='args')

        data = self.parser.parse_args()

        whereData = query(data['query']) if 'query' in data and data['query'] is not None else {}
        paramData = {
            'page': int(data['page']) if data['page'] is not None else 1,
            'limit': int(data['limit']) if data['limit'] is not None else 10,
        }

        queryData, queryPagination = self.getAllData(whereData, paramData)
        return self.api_response.success('get', queryData, queryPagination, startTime=self.startTime)


    def post(self):
        return notFound(self.api_response.failed)


    def put(self):
        return notFound(self.api_response.failed)


    def delete(self):
        return notFound(self.api_response.failed)

# ---------------------------------------------------------------------------------------------------------------------

    def getAllData(self, query, params):
        return self.users.getAll(query, params)

# ---------------------------------------------------------------------------------------------------------------------

def startUsers(api, config, api_response, mongo_connection):
    api.add_resource(CoreUsers, '/v1/core/users', endpoint = 'users', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
