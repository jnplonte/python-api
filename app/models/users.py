from app.models import Models

class Users(Models):
    __tablename__ = 'users'
    __columns__ = ['_id', 'firstName', 'lastName', 'email', 'phone', 'userName', 'salt', 'password', 'forgotPasswordKey', 'passwordExpiry', 'loginAttempt', 'lastLogin', 'active', 'createdAt']

    def __init__(self, Connection):
        super().__init__(Connection, self.__tablename__, self.__columns__)
    
