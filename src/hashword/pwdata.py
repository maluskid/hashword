import hashlib
import base64
import random


def seed_generator():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', '/', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                'g', 'h', 'i', '=', 'j', 'k', 'l', '+', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't', 'u', '-', 'v', 'w', 'x', 'y',
                'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    random.seed()
    rstring = ''
    length = random.randrange(24, 32)
    for i in range(length):
        index = random.randrange(66)
        rstring += alphabet[index]
    return base64.encodebytes(rstring.encode()).decode()


class PwData:

    def __init__(self, data):
        self.hash_alg = data['algo']
        self.name = data['name']
        self.seed = data['seed']
        self.size = data['size']

    def getpw(self, verbose=False):
        h = None
        match self.hash_alg:
            case 'sha256':
                h = hashlib.sha256()
            case 'sha-3':
                h = hashlib.shake_256()
            case 'blake2b':
                h = hashlib.blake2b()
            case 'md5':
                h = hashlib.md5()
            case _:
                raise (Exception(
                    "PwData object corrupted or improperly formatted."))

        h.update(self.seed.encode())
        temp = h.hexdigest()
        if verbose:
            print("Printing the first {size} characters of hash for {name}"
                  .format(size=self.size, name=self.name))
        out = ''
        for i in range(self.size):
            out += temp[i]

        return out
