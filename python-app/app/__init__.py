import os
import base64
import datetime

from flask import Flask, jsonify, g
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, abort, request

from app import config
from app.services.api_response import ApiResponse

from app.v1.authentication.token import startToken


env = os.environ.get('ENV')

if env == 'development':
    configs = config.DevConfig
elif env == 'production':
    configs = config.ProdConfig
else:
    configs = config.LocalConfig

print('api environment is %s', env.upper())
print('api listening to http://localhost:%s', os.environ.get('PORT'))

# ---------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://%s:%s@%s:%i/%s' % (configs.MONGO_USERNAME, configs.MONGO_PASSWORD, configs.MONGO_HOST, configs.MONGO_PORT, configs.MONGO_DATABASE)

mongo = PyMongo(app)
api = Api(app)


@app.before_request
def tokenCheck():
    if request.method == 'OPTIONS':
        return

    # request_token = request.headers.get(configs.SECRET_KEY, None)
    
    # query_string = request.args.get(configs.SECRET_KEY, None)
    # if query_string is not None:
    #     try:
    #         request_token = base64.b64decode(query_string).decode('utf-8')
    #     except Exception as e:
    #         response = jsonify(api_response.failed('server', e))
    #         response.status_code = 500

    #         return response

    # secret_key = configs.SECRET_KEY_HASH.split(',')

    # if request_token is None or request_token not in secret_key:
    #     response = jsonify(api_response.failed('authentication', ''))
    #     response.status_code = 401

    #     return response

    user_data = {}

    user_string = request.headers.get(configs.SECRET_KEY, None)

    if user_string is None:
        response = jsonify(api_response.failed('authentication', ''))
        response.status_code = 401

        return response

    if '/v1/' in request.url:
        # customer_data = Customers(mongo, False).get({'key': str(customer_string)})
        # if len(customer_data) == 0:
        #     response = jsonify(api_response.failed('invalid-customer-key', ''))
        #     response.status_code = 401

        #     return response
        print('v1 here')
    else:
        if user_string != configs.SECRET_KEY_HASH:
            response = jsonify(api_response.failed('authentication', ''))
            response.status_code = 401

            return response
        
    g.user = user_data


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

if __name__ == "__main__":
	app.run(debug=True)