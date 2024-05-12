from cryptography.fernet import Fernet
import base64
import getpass
import hashlib
import os
import pickle
import random
import rsa
import stat


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
            case 'sha-3':
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


user = getpass.getuser().strip()
PATH = os.path.join('home', user, '.hashword/')
os.makedirs(os.path.join(PATH, 'Keys/'), exist_ok=True)
os.makedirs(os.path.join(PATH, 'Data/'), exist_ok=True)
# if os.stat(os.path.join(PATH, 'Data/', 'alias.json'))


class HashWord(dict):

    def populate(self):
        # loads every saved password in one go
        dirpath = os.path.join(PATH, 'Data/')
        for file in os.listdir(dirpath):
            if not file.endswith('.json', '.bak'):
                filepath = os.path.join(dirpath, file)
                with open(filepath, 'rb') as f:
                    item = pickle.load(f)
                    self[item.name] = item

    def load(self, name):
        # loads a specific password
        filepath = os.path.join(PATH, 'Data/', name)
        with open(filepath, 'rb') as f:
            item = pickle.load(f)
            self[item.name] = item

    def save(self):
        dirpath = os.path.join(PATH, 'Data/')
        for key in self:
            filepath = os.path.join(dirpath, self[key].name)
            with open(filepath, 'wb') as f:
                pickle.dump(self[key], f)

    def create(self, name, size, algo, seed):
        match algo:
            case '1':
                if size > 64:
                    size = 64
                if len(seed) > 0:
                    self[name] = PwData(name, size, seed=seed + '\n')
                else:
                    self[name] = PwData(name, size)
            case '2':
                if size > 32:
                    size = 32
                if len(seed) > 0:
                    self[name] = PwData(
                        name, size, seed=seed + '\n', alg='md5')
                else:
                    self[name] = PwData(name, size, alg='md5')
            case '3':
                if size > 32:
                    size = 32
                if len(seed) > 0:
                    self[name] = PwData(
                        name, size, seed=seed + '\n', alg='sha-3')
                else:
                    self[name] = PwData(name, size, alg='sha-3')
            case '4':
                if size > 64:
                    size = 64
                if len(seed) > 0:
                    self[name] = PwData(
                        name, size, seed=seed + '\n', alg='blake2b')
                else:
                    self[name] = PwData(name, size, alg='blake2b')
            case _:
                print("Algorithm selection not recognized." +
                      "Defaulting to sha256\n.")
                if size > 64:
                    size = 64
                if len(seed) > 0:
                    self[name] = PwData(name, size, seed=seed + '\n')
                else:
                    self[name] = PwData(name, size)

    def list_self(self):
        count = 0
        for key in self:
            count += 1
            aliases = ''
            for item in self[key].alias_list:
                aliases += (item + ' ')
            cstr = str(count) + ")\t" + key + "\n\t- aliases: " + aliases
            print(cstr)

    def delete(self, arg):
        for file in
        filepath = os.path.join(PATH, "Data/", name)
        try:
            os.remove(filepath)
        except OSError as e:
            print(e, "Encountered deleting")
        self.pop(name)
