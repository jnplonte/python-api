import math
import pymongo

from datetime import datetime, timezone, timedelta
from bson.objectid import ObjectId

class Models():
    __tablename__ = None
    __columns__ = []

    def __init__(self, Connection, tableName, columns, unique = None, seed = False):
        if seed is True:
            self.connection = Connection[tableName]
        else:
            self.connection = Connection.db[tableName]

        if unique is not None:
            for uData in unique:
                self.connection.create_index(uData, unique=True)
        
        self.__tablename__ = tableName
        self.__columns__ = columns


    def getAll(self, query, params = {}, fields = []):
        finalFields = {}
        for fld in fields:
            finalFields[fld] = 1

        if bool(finalFields) is False:
            finalFields = None

        page = int(params['page']) if 'page' in params else 1
        limit = int(params['limit']) if 'limit' in params else 10

        offset = limit * (page - 1);

        self.printLogs('GET', query, '')
        documentCount = self.connection.count_documents(query)
        document = self.connection.find(query, finalFields, sort=[('createdAt', -1)]).skip(offset).limit(limit)

        if document is None:
            return (list(), {})

        return (list(self.cleanColumnArray(document)), {
            'totalData': int(documentCount),
            'totalPage': math.ceil(int(documentCount) / limit),
            'currentPage': page
        })


    def getCount(self, query):
        self.printLogs('GET', query, '')
        documentCount = self.connection.count_documents(query)

        if documentCount is None:
            return int(0)

        return int(documentCount)


    def getAllFields(self, query, fields = []):
        finalFields = {}
        for fld in fields:
            finalFields[fld] = 1

        if bool(finalFields) is False:
            finalFields = None

        self.printLogs('GET', query, '')
        document = self.connection.find(query, finalFields)

        if document is None:
            return list()

        return list(self.cleanColumnArray(document))


    def getById(self, id, fields = []):
        finalFields = {}
        for fld in fields:
            finalFields[fld] = 1

        if bool(finalFields) is False:
            finalFields = None

        self.printLogs('GET', {'_id': id}, '')
        document = self.connection.find_one({'_id': ObjectId(id)}, finalFields)

        if document is None:
            return dict()

        return dict(self.cleanColumns(document))


    def get(self, query, fields = []):
        finalFields = {}
        for fld in fields:
            finalFields[fld] = 1

        if bool(finalFields) is False:
            finalFields = None

        self.printLogs('GET', query, '')
        document = self.connection.find_one(query, finalFields, sort=[('createdAt', -1)])

        if document is None:
            return dict()

        return dict(self.cleanColumns(document))


    def save(self, data):
        data['updatedAt'] = self.getCurrentDate()
        data['createdAt'] = self.getCurrentDate()

        self.printLogs('INSERT', '', data)
        document = self.connection.insert_one(self.filterColumns(data)).inserted_id
        return str(document)


    def saveAll(self, data):
        finalDocument = []
        for (dataIndex1, dataValue1) in enumerate(data):
            dataValue1['updatedAt'] = self.getCurrentDate()
            dataValue1['createdAt'] = self.getCurrentDate()

        self.printLogs('INSERT', '', data)
        try:
            document = self.connection.insert_many(self.filterColumnArray(data), ordered=False)
            finalIds = []
            for doc in document.inserted_ids:
                finalIds.append(str(doc))

            return finalIds

        except pymongo.errors.BulkWriteError as e:
            if e.details['nInserted'] >= 1:
                errorIds = []
                for eIndx, eData in enumerate(e.details['writeErrors']):
                    if 'op' in eData and bool(eData['op']):
                        errorIds.append(str(eData['op']['_id']))

                finalIds = []
                for dIndx, dData in enumerate(data):
                    if str(dData['_id']) not in errorIds:
                        finalIds.append(str(dData['_id']))

                return finalIds
            else:
                return []


    def updateById(self, id, data):
        data['updatedAt'] = self.getCurrentDate()

        self.printLogs('UPDATE', {'_id': id}, data)
        document = self.connection.find_one_and_update({'_id': ObjectId(id)}, {'$set': self.filterColumns(data)}, new=True)
        
        if document is None:
            return dict()

        return dict(self.cleanColumns(document))


    def pushById(self, id, data):
        self.printLogs('UPDATE', {'_id': id}, data)
        document = self.connection.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'updatedAt': self.getCurrentDate()}, '$addToSet': self.filterColumns(data)}, new=True)
        
        if document is None:
            return dict()

        return dict(self.cleanColumns(document))


    def incrementById(self, id, data):
        self.printLogs('UPDATE', {'_id': id}, data)
        document = self.connection.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'updatedAt': self.getCurrentDate()}, '$inc': self.filterColumns(data)}, new=True)
        
        if document is None:
            return dict()

        return dict(self.cleanColumns(document))


    def update(self, query, data):
        data['updatedAt'] = self.getCurrentDate()

        self.printLogs('UPDATE', query, data)
        document = self.connection.find_one_and_update(query, {'$set': self.filterColumns(data)}, new=True)
        
        if document is None:
            return dict()

        return dict(self.cleanColumns(document))

    def updateAll(self, query, data):
        data['updatedAt'] = self.getCurrentDate()

        self.printLogs('UPDATE', query, data)
        document = self.connection.update(query, {'$set': self.filterColumns(data)}, multi=True)
        return str(document)


    def deleteById(self, id):
        self.printLogs('DELETE', {'_id': id}, '')
        document = self.connection.delete_one({'_id': ObjectId(id)}).deleted_count
        return str(document)


    def delete(self, query):
        self.printLogs('DELETE', query, '')
        document = self.connection.delete_one(query).deleted_count
        return str(document)


    def deleteAll(self, query):
        self.printLogs('DELETE', query, '')
        document = self.connection.delete_many(query).deleted_count
        return str(document)


    def filterColumns(self, document):
        finalData = {}
        for dataValue in document:
            if dataValue in self.__columns__:
                finalData[dataValue] = document[dataValue]

        return finalData


    def filterColumnArray(self, document):
        finalData = []
        for doc in document:
            finalData.append(self.filterColumns(doc))
        
        return finalData


    def cleanColumns(self, document):
        finalData = {}
        for doc in document:
            if doc in self.__columns__:
                if isinstance(document[doc], datetime) or ObjectId.is_valid(document[doc]):
                    fData = str(document[doc])
                else:
                    fData = document[doc]

                finalData[doc] = fData

        return finalData


    def cleanColumnArray(self, document):
        finalData = []
        for doc in document:
            finalData.append(self.cleanColumns(doc))

        return finalData

    def getCurrentDate(self):
        return str(datetime.now(timezone(timedelta(hours=8)))).replace('+08:00', '')

    def printLogs(self, type='', query='', data=''):
        print('==================================================')
        print('LOG TYPE:', type)
        print('LOG TABLE:', self.__tablename__)
        print('LOG TIME:', self.getCurrentDate())
        print('LOG QUERY:', query)
        print('LOG DATA:', data)
        print('==================================================')
