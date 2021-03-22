import config
from bson.objectid import ObjectId

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from app.models.users import Users

def columns():
    return ['_id', 'key', 'code', 'firstName', 'lastName', 'email', 'phone', 'active', 'updatedAt', 'createdAt']
    
def data():
    return [
        { 'key': 'Lrzu8gKFu3Q9346pEgcE4eFBrFYsE95JS6Zsgecu6LFYa7yr2D', 'code': 'USER00001', 'firstName': 'jnpl', 'lastName': 'onte', 'email': 'jnpl.onte@gmail.com'},
        { 'key': 'CUNcbvFasENq69kRpxx8femgLj4LUZDnYsAt7HYWFT7ZMjeuvL', 'code': 'SPIDERMAN', 'firstName': 'peter', 'lastName': 'parker', 'email': 'spiderman@gmail.com'}
    ]

def seed(mongo):
    users = Users(mongo, True)

    document = users.saveAll(data())
    return document

if __name__ == '__main__':
    mongoClient = config.mongoConnect()
    
    print('start seed')

    document = seed(mongoClient)
    print(document)
    
    print('end seed')
