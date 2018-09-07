
def removeDuplicate(objectList):
    seen = set()
    newObjectList = []
    for ordr in objectList:
        t = tuple(ordr.items())
        if t not in seen:
            seen.add(t)
            newObjectList.append(ordr)
    
    return newObjectList