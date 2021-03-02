import datetime

from pymongo import MongoClient, errors

def mongoConnect():
    MONGO_HOST = ''
    MONGO_PORT = 0
    MONGO_DATABASE = ''
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''

    try:
        if MONGO_PASSWORD == '':
            client = MongoClient('mongodb://%s@%s:%i/%s' % (MONGO_USERNAME, MONGO_HOST, MONGO_PORT, MONGO_DATABASE))
        else:
            client = MongoClient('mongodb://%s:%s@%s:%i/%s' % (MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DATABASE))
        
        print('mongodb://%s:%s@%s:%i/%s' % (MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DATABASE))
        print("server_info():", client.server_info())
        
    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR:", err)

    return client.get_default_database()

if __name__ == '__main__':
    print('mongo start')

    mongoClient = mongoConnect()
    print(mongoClient)
    
    print('mongo end')