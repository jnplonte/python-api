from datetime import datetime

from flask_restful import Resource, reqparse

from app.services.query import query
from app.services.not_found import notFound
from app.services.remove_none import removeNone

from app.models.users import Users

class CoreUser(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.startTime = datetime.now()

        self.api_response = api_response

        self.users = Users(mongo_connection, False)

        self.parser = reqparse.RequestParser()


    """
    @api {get} /core/user/:id get user
    @apiVersion 1.0.0
    @apiName get
    @apiGroup USERS
    @apiPermission authenticated-user
    @apiDescription get user
    
    @apiParam (url segment) {String} id user id
    @apiParam (url parameter) {String} key key search Ex. ?key=name
    """
    def get(self, id=None):
        self.parser.add_argument('key', type=str, location='args', default='_id')

        data = self.parser.parse_args()

        try:
            queryData = self.getOneData(data['key'], id)
            return self.api_response.success('get', queryData, startTime=self.startTime)
        except Exception as e:
            return self.api_response.failed('get', str(e))


    def post(self, id=None):
        return notFound(self.api_response.failed)


    """
    @api {put} /core/user/:id update user
	@apiVersion 1.0.0
	@apiName put
	@apiGroup USERS
	@apiPermission authenticated-user
	@apiDescription update user

    @apiParam (url segment) {String} id user id
    @apiParam (body) {String} [code] user code
    @apiParam (body) {String} [firstName] first name
    @apiParam (body) {String} [lastName] last name
    @apiParam (body) {String} [email] unique email address
    @apiParam (body) {String} [phone] unique phone number
    @apiParam (body) {Boolean} [active] is active user
    """
    def put(self, id=None):
        self.parser.add_argument('code', type=str)
        self.parser.add_argument('firstName', type=str)
        self.parser.add_argument('lastName', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('phone', type=str)
        self.parser.add_argument('active', type=bool)

        data = self.parser.parse_args()

        try:
            updateData = self.updateOneData(data, id)
            if not bool(updateData):
                return self.api_response.failed('put', '')
    
            return self.api_response.success('put', updateData, startTime=self.startTime)
        except Exception as e:
            return self.api_response.failed('put', str(e))


    """
    @api {delete} /core/user/:id delete user
	@apiVersion 1.0.0
	@apiName delete
	@apiGroup USERS
	@apiPermission authenticated-user
	@apiDescription delete user

    @apiParam (url segment) {String} id user id
    @apiParam (url parameter) {Boolean} force is force delete Ex. ?force=true
    """
    def delete(self, id=None):
        self.parser.add_argument('force', type=bool, default=False)

        data = self.parser.parse_args()

        try:
            deleteData = self.deleteOneData(data['force'], id)
            if not bool(deleteData):
                return self.api_response.failed('delete', '')

            return self.api_response.success('delete', deleteData, startTime=self.startTime)
        except Exception as e:
            return self.api_response.failed('delete', str(e))

# ---------------------------------------------------------------------------------------------------------------------
    def getOneData(self, key, kId):
        if key == '_id':
            return self.users.getById(kId)
        else:
            return self.users.get({key: kId})

    def updateOneData(self, data, kId):
        return self.users.updateById(kId, removeNone(data))

    def deleteOneData(self, force, kId):
        if force is True:
            return self.users.deleteById(kId)
        else:
            return self.users.updateById(kId, {'active': False})
# ---------------------------------------------------------------------------------------------------------------------

def startUser(api, config, api_response, mongo_connection):
    api.add_resource(CoreUser, '/v1/core/user/<string:id>', endpoint = 'user', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
