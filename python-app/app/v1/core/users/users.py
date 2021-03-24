from datetime import datetime

from flask_restful import Resource, reqparse

from app.services.query import query
from app.services.not_found import notFound
from app.services.generate_key import generateKey

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
    @apiName all
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


    """
    @api {post} /core/users insert user
    @apiVersion 1.0.0
    @apiName post
    @apiGroup USERS
    @apiPermission authenticated-user
    @apiDescription insert user

    @apiParam (body) {String} code user code
    @apiParam (body) {String} firstName first name
    @apiParam (body) {String} lastName last name
    @apiParam (body) {String} email unique email address
    @apiParam (body) {String} phone unique phone number
    """
    def post(self):
        self.parser.add_argument('code', type=str)
        self.parser.add_argument('firstName', type=str)
        self.parser.add_argument('lastName', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('phone', type=str, default=None)

        data = self.parser.parse_args()

        if self.checkRequiredPostParameters(data) is False:
            return self.api_response.failed('data', ['code', 'firstName', 'lastName', 'email'])

        try:
            saveId = self.saveOneData(data)
            if not bool(saveId):
                return self.api_response.failed('post', '')

            return self.api_response.success('post', saveId, startTime=self.startTime)
        except Exception as e:
            return self.api_response.failed('post', str(e))


    def put(self):
        return notFound(self.api_response.failed)


    def delete(self):
        return notFound(self.api_response.failed)

# ---------------------------------------------------------------------------------------------------------------------
    def checkRequiredPostParameters(self, data):
        if data['code'] is None or data['firstName'] is None or data['lastName'] is None or data['email'] is None:
            return False
        
        return True

    def getAllData(self, query, params):
        return self.users.getAll(query, params)

    def saveOneData(self, data):
        data['active'] = True
        data['key'] = generateKey(50)

        return self.users.save(data)
# ---------------------------------------------------------------------------------------------------------------------

def startUsers(api, config, api_response, mongo_connection):
    api.add_resource(CoreUsers, '/v1/core/users', endpoint = 'users', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
