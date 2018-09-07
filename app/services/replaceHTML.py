
def replaceHTML(dataString, dataObject):
    for data in dataObject:
        dataString = dataString.replace('{{' + data + '}}', dataObject[data])
        
    return dataString