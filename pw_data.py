import hashlib
import  random

def seed_generator():
    alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    random.seed()
    out = ''
    for i in range(24):
        index = random.randrange(36)
        out += alphabet[index]
    return out

class PwData:

    def __init__(self, name, size, alg='sha256', seed=seed_generator()):
        self.name = name
        self.size = size
        self.hash_alg = alg
        self.seed = seed
        self.alias_list = list()

    def add_alias(self, alias):
        self.alias_list.append(alias)

    def getpw(self):
        h = None
        match self.hash_alg:
            case 'sha128':
                h = hashlib.shake_256()
            case 'blake2b':
                h = hashlib.blake2b()
            case 'md5':
                h = hashlib.md5()
            case _:
                h = hashlib.sha256()

        h.update(self.seed.encode())
        temp = h.hexdigest()
        print("Printing the first {size} characters of hash for {name}"
              .format(size=self.size, name=self.name))
        out = ''
        for i in range(self.size):
            out += temp[i]

        return out


