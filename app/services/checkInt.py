def checkInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False