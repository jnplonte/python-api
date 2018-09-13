import hashlib

from app.services.checkInt import checkInt
from app.services.randomString import randomString

def getQuery(reqParams):
    query = reqParams['query'].split('|') if 'query' in reqParams else []
    queryParams = {}
    for param in query:
        qParam = param.split(':')
        queryParams[qParam[0]] = int(qParam[1]) if checkInt(qParam[1]) else qParam[1]

    return queryParams

def getPassword(password):
    salt = randomString(6)
    hashPassword = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    return (salt, hashPassword)
