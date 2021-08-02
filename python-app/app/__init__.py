import os
import base64
import datetime

from flask import Flask, jsonify, g
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, abort, request

from app import config
from app.services.api_response import ApiResponse

from app.v1.authentication.token import startToken

from app.v1.core.users.user import startUser
from app.v1.core.users.users import startUsers

from app.models.users import Users

env = os.environ.get('ENV')
port = os.environ.get('PORT')

if env == 'development':
    configs = config.DevConfig
elif env == 'production':
    configs = config.ProdConfig
else:
    configs = config.LocalConfig

print('api environment is %s' % env.upper() if env is not None else 'local')
print('api listening to http://localhost:%s' % os.environ.get('PORT') if env is not None else '8383' )

# ---------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://%s:%s@%s:%i/%s' % (configs.MONGO_USERNAME, configs.MONGO_PASSWORD, configs.MONGO_HOST, configs.MONGO_PORT, configs.MONGO_DATABASE)

mongo = PyMongo(app)
api = Api(app)


@app.before_request
def tokenCheck():
    if request.method == 'OPTIONS':
        return

    userData = {}
    userString = request.headers.get(configs.SECRET_KEY, None)

    if userString is None:
        response = jsonify(api_response.failed('authentication', ''))
        response.status_code = 401

        return response

    if 'auth' in request.url:
        if userString != configs.SECRET_KEY_HASH:
            response = jsonify(api_response.failed('authentication', ''))
            response.status_code = 401

            return response
    else:
        if userString != configs.SECRET_KEY_HASH:
            response = jsonify(api_response.failed('authentication', ''))
            response.status_code = 401

            return response

        userData = Users(mongo, False).get({'key': str(request.args.get('user-key'))})
        if not bool(userData):
            response = jsonify(api_response.failed('authentication', ''))
            response.status_code = 401

            return response

    g.user = userData


@app.after_request
def corsCheck(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')

    return response


@app.errorhandler(404)
def not_found(error):
    response = jsonify(api_response.failed('notfound', ''))
    response.status_code = 404

    return response


api_response = ApiResponse()

startToken(api, configs, api_response, mongo)

startUser(api, configs, api_response, mongo)
startUsers(api, configs, api_response, mongo)

if __name__ == "__main__":
	app.run(debug=True)