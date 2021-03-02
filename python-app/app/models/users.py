from pymongo import DESCENDING

from app.models import Models

class Users(Models):
    __tablename__ = 'users'
    __columns__ = ['_id', 'key', 'code', 'firstName', 'lastName', 'email', 'phone', 'active', 'updatedAt', 'createdAt']
    __unique__ = [[('code', DESCENDING)]]


    def __init__(self, Connection, seed = False):
        super().__init__(Connection, self.__tablename__, self.__columns__, self.__unique__, seed=seed)
        print('users mongo init')
