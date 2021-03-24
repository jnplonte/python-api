import random
import string

def generateKey(length=50):
    lettersAndDigits = string.ascii_letters + string.digits
    randomKey = ''.join((random.choice(lettersAndDigits) for i in range(length)))

    return randomKey