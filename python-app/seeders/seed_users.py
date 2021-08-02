import base
from bson.objectid import ObjectId

import sys
sys.path.append('/application')

from app.models.users import Users

def columns():
    return [
        '_id',
        'key',
        'code',
        'firstName',
        'lastName',
        'email',
        'phone',
        'active',
        'updatedAt',
        'createdAt'
    ]
    
def data():
    return [
        { 
            "_id": ObjectId("61076b8d140a70fbddd4ef30"),
            'key': 'Lrzu8gKFu3Q9346pEgcE4eFBrFYsE95JS6Zsgecu6LFYa7yr2D', 
            'code': 'USER00001',
            'firstName': 'jnpl',
            'lastName': 'onte',
            'email': 'jnpl.onte@gmail.com'
        },
        { 
            "_id": ObjectId("61076b92413af0851ab15323"),
            'key': 'CUNcbvFasENq69kRpxx8femgLj4LUZDnYsAt7HYWFT7ZMjeuvL',
            'code': 'SPIDERMAN',
            'firstName': 'peter',
            'lastName': 'parker',
            'email': 'spiderman@gmail.com'
        }
    ]

def seed(mongo):
    users = Users(mongo, True)

    document = users.saveAll(data())
    return document


if __name__ == '__main__':
    mongoClient = base.mongoConnect()
    
    print('start seeding')

    document = seed(mongoClient)
    print(document)
    
    print('end seeding')
