
def query(data):
    finalQuery = {}
    query = data.split('|')

    if len(query) >= 1:
        for qData in query:
            if (qData.find(':') != -1):
                qDataFinal = qData.split(':')
                if (qDataFinal[1].find(',') != -1):
                    arrQDataFinal = {'$in': qDataFinal[1].split(',')}
                else:
                    arrQDataFinal = qDataFinal[1]

                finalQuery[qDataFinal[0]] = arrQDataFinal
    
    return finalQuery