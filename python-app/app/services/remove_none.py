def removeNone(data):
    dataLoop = data.copy();
    for dKey, dVal in dataLoop.items():
        if dVal is None:
            del data[dKey]

    return data