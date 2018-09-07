import logging
import falcon

from falcon_cors import CORS

import app.services.serialization as json


from app.config import LocalConfig, DevConfig, ProdConfig, configs
from app.middleware import JSONTranslator, TokenValidation

from app.services.logs import setupLogging
from app.services.mongo import mongoConnect

from app.resources.users import UsersResources

def create_app(env, **kwargs):
    if env == 'LOCAL':
        configs = LocalConfig
    elif env == 'DEV':
        configs = DevConfig
    elif env == 'PROD':
        configs = ProdConfig
    else:
        configs = LocalConfig

    log_level = kwargs.get('log_level', configs.LOG_LEVEL)
    setupLogging(log_level)

    logger = logging.getLogger(configs.APP_NAME)
    logger.info('Starting {} in {} mode'.format(configs.APP_NAME, configs.ENV))

    cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)

    app = falcon.API(
        middleware=[
            cors.middleware,
            TokenValidation(configs),
            JSONTranslator(configs)
        ]
    )

    create_route(app, configs)
    return app


def create_route(app, configs):
    mongoConnection = mongoConnect(configs)

    app.add_route('/v1/users', UsersResources(configs, mongoConnection))
    app.add_route('/v1/users/{id}', UsersResources(configs, mongoConnection))
