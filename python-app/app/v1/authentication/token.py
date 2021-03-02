from datetime import datetime

from flask_restful import Resource, reqparse

from app.services.not_found import notFound

from app.models.users import Users

class AuthenticationToken(Resource):
    def __init__(self, config, api_response, mongo_connection):
        self.config = config
        self.startTime = datetime.now()

        self.api_response = api_response

        self.users = Users(mongo_connection, False)

        self.parser = reqparse.RequestParser()


    def get(self):
        return notFound(self.api_response.failed)


    """
    @api {post} /auth/token fetch user information
    @apiVersion 1.0.0
    @apiName post-token
    @apiGroup AUTHENTICATION
    @apiPermission all
    @apiDescription fetch user information via token

    @apiParam (body) {String} key user key
    """
    def post(self):
        self.parser.add_argument('key', type=str)

        data = self.parser.parse_args()

        if self.checkRequiredPostParameters(data) is False:
            return self.api_response.failed('data', ['key'])

        try:
            queryData = self.getData(data['key'])
            if not bool(queryData):
                return self.api_response.failed('token', '')
    
            return self.api_response.success('token', queryData, startTime=self.startTime)
        except Exception as e:
            return self.api_response.failed('token', str(e))


    def put(self):
        return notFound(self.api_response.failed)


    def delete(self):
        return notFound(self.api_response.failed)

# ---------------------------------------------------------------------------------------------------------------------

    def checkRequiredPostParameters(self, data):
        if data['key'] is None:
            return False
        
        return True

    def getData(self, kId):
        return self.users.get({'key': kId})

# ---------------------------------------------------------------------------------------------------------------------

def startToken(api, config, api_response, mongo_connection):
    api.add_resource(AuthenticationToken, '/v1/auth/token', endpoint = 'token', resource_class_kwargs={'config': config, 'api_response': api_response, 'mongo_connection': mongo_connection})
