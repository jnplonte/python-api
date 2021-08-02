import os

class BaseConfig(object):
    APP_NAME = 'pythonapi'
    LOGO = 'https://via.placeholder.com/50'
    SECRET_KEY = 'x-python-api-key'
    SECRET_KEY_HASH = 'KuQmvnxXEjR7KXwfucgerTf6YwZV5Amz5awwxf5PFgkpGrb3Jn'
    GET_QUERY_LIMIT = 10

    LOG_LEVEL = 'DEBUG'

    MONGO_HOST = ''
    MONGO_PORT = 0
    MONGO_DATABASE = ''
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''


class LocalConfig(BaseConfig):
    LOG_LEVEL = 'DEBUG'

    MONGO_HOST = '192.168.1.4'
    MONGO_PORT = 27018
    MONGO_DATABASE = 'testDB'
    MONGO_USERNAME = 'admin'
    MONGO_PASSWORD = 'johnpaul'


class DevConfig(BaseConfig):
    LOG_LEVEL = 'DEBUG'

    MONGO_HOST = os.getenv('MONGO_HOST', '')
    MONGO_PORT = os.getenv('MONGO_PORT', 0)
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', '')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')


class ProdConfig(BaseConfig):
    LOG_LEVEL = 'INFO'

    MONGO_HOST = os.getenv('MONGO_HOST', '')
    MONGO_PORT = os.getenv('MONGO_PORT', 0)
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', '')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
