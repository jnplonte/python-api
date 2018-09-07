import logging

from pymongo import MongoClient

import app.services.serialization as json

def mongoConnect(configs):
    if configs.MONGO_PASSWORD == '':
        client = MongoClient('mongodb://%s@%s:%i/%s' % (configs.MONGO_USERNAME, configs.MONGO_HOST, configs.MONGO_PORT, configs.MONGO_DATABASE))
    else:
        client = MongoClient('mongodb://%s:%s@%s:%i/%s' % (configs.MONGO_USERNAME, configs.MONGO_PASSWORD, configs.MONGO_HOST, configs.MONGO_PORT, configs.MONGO_DATABASE))
    
    logger = logging.getLogger(configs.APP_NAME)
    logger.info('connected to mongo database')

    return client.get_default_database()
