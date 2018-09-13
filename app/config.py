import os

class BaseConfig(object):
    APP_NAME = 'python-api'
    VERSION = 'v1'
    SECRET_KEY = 'x-python-api-key'
    SECRET_KEY_HASH = '$someSecretKeyHere$'
    SECRET_KEY_LENGTH = 5
    GET_QUERY_LIMIT = 10
    LOGO = 'https://www.logo.com/img.png'

    ENV = ''
    LOG_LEVEL = ''

    MONGO_HOST = ''
    MONGO_PORT = 0
    MONGO_DATABASE = ''
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''


class LocalConfig(BaseConfig):
    ENV = 'LOCAL'
    LOG_LEVEL = 'DEBUG'

    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DATABASE = 'testDB'
    MONGO_USERNAME = 'admin'
    MONGO_PASSWORD = 'johnpaul'


class DevConfig(BaseConfig):
    ENV = 'DEV'
    LOG_LEVEL = 'DEBUG'

    MONGO_HOST = os.getenv('MONGO_HOST', '')
    MONGO_PORT = os.getenv('MONGO_PORT', 0)
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', '')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')


class ProdConfig(BaseConfig):
    ENV = 'PROD'
    LOG_LEVEL = 'INFO'

    MONGO_HOST = os.getenv('MONGO_HOST', '')
    MONGO_PORT = os.getenv('MONGO_PORT', 0)
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', '')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')


configs = LocalConfig
