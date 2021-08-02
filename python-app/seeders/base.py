
import datetime
from pymongo import MongoClient, errors

import sys
sys.path.append('/application')

from app import config

def mongoConnect():
    configs = config.LocalConfig

    try:
        client = MongoClient('mongodb://%s:%s@%s:%i/%s' % (configs.MONGO_USERNAME, configs.MONGO_PASSWORD, configs.MONGO_HOST, configs.MONGO_PORT, configs.MONGO_DATABASE))        
        print('mongodb://%s:%s@%s:%i/%s' % (configs.MONGO_USERNAME, configs.MONGO_PASSWORD, configs.MONGO_HOST, configs.MONGO_PORT, configs.MONGO_DATABASE))
        print("server_info():", client.server_info())
        
    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR:", err)

    return client.get_default_database()

if __name__ == '__main__':
    print('mongo seed start')

    mongoClient = mongoConnect()
    print(mongoClient)