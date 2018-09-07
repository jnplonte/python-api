import datetime
import math

from bson import ObjectId, json_util

class Models():
    __tablename__ = None
    __columns__ = []

    def __init__(self, Connection, tableName, columns):
        self.connection = Connection[tableName]
        
        self.__tablename__ = tableName
        self.__columns__ = columns
        self.defaultColumns = self.getDefaultColumns()
    

    def getAll(self, query, params = {}):
        page = int(params['page']) if 'page' in params else 1
        limit = int(params['limit']) if 'limit' in params else 10

        offset = limit * (page - 1)

        documentCount = self.connection.count(query)
        document = self.connection.find(query, sort=[('createdAt', -1)]).skip(offset).limit(limit)

        if document is None:
            return (dict(), {})

        return (self.cleanColumnArray(document), {
            'totalData': int(documentCount),
            'totalPage': math.ceil(int(documentCount) / limit),
            'currentPage': page
        })


    def getById(self, id):
        document = self.connection.find_one({'_id': ObjectId(id)})

        if document is None:
            return dict()

        return self.cleanColumns(document)


    def get(self, query):
        document = self.connection.find_one(query, sort=[('createdAt', -1)])

        if document is None:
            return dict()

        return self.cleanColumns(document)


    def save(self, data):
        data['createdAt'] = datetime.datetime.utcnow()

        document = self.connection.insert_one({**self.defaultColumns, **self.filterColumns(data)}).inserted_id
        return str(document)


    def updateById(self, id, data):
        self.connection.update_one({'_id': ObjectId(id)}, {'$set': self.filterColumns(data)}, True)
        return str(id)


    def update(self, query, data):
        document = self.connection.update_one(query, {'$set': self.filterColumns(data)}, True)
        return str(document)


    def getDefaultColumns(self):
        defaults = {
            'active': True,
            'createdAt': datetime.datetime.utcnow()
        }
        data = dict()

        for col in self.__columns__:
            if col != '_id':
                data[col] = defaults.get(col, '')

        return data

    def filterColumns(self, data):
        finalData = dict()
        for dataValue in data:
            if dataValue in self.__columns__:
                finalData[dataValue] = data[dataValue]

        return finalData


    def cleanColumns(self, document):
        finalData = dict()
        for doc in document:
            if doc in self.__columns__:
                if isinstance(document[doc], datetime.datetime) or ObjectId.is_valid(document[doc]):
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
