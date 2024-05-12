from cryptography.fernet import Fernet
import base64
import getpass
import hashlib
import os
import pickle
import random
import rsa
import stat
import json


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

    def get(self, target):
        manifestpath = os.path.join(PATH, "Data/manifest.json")
        try:
            with open(manifestpath, 'r') as m:
                manifest = json.load(m)
        except Exception as e:
            raise (e)
            match manifest:
                case {"passwords": name} if name == target:
                    name = target
                    filepath = os.path.join(PATH, "Data/", target)
                case {"aliases": alias} if alias == target:
                    name = manifest["aliases"][alias]["references"]
                    filepath = os.path.join(PATH, "Data/", name)
                case _:
                    raise (KeyError)
        print(filepath)

    def create(self, name, seed, size, algo):
        match [size, algo]:
            case [size_val, ('blake2b' | 'sha256')]:
                if size_val > 64 or not size_val:
                    size_val = 64
            case [size_val, ('md5' | 'sha-3')]:
                if size > 32 or not size_val:
                    size_val = 32
            case [size_val, _]:
                print("Algorithm selection not recognized." +
                      "Defaulting to sha256.\n")
                algo = 'sha256'
                if size_val > 64 or not size_val:
                    size_val = 64
        match [seed, len(seed)]:
            case [seed_val, length] if length > 4 and seed_val:
                seed_val += '\n'
                self[name] = PwData(name, size_val, seed=seed_val, alg=algo)
            case [seed_val, length] if length <= 4 and seed_val:
                raise (ValueError("Seed must be at least 5 characters in \
                    length. Creating a password without a seed will default \
                    to a randomly generated one."))
            case [seed_val, _] if not seed_val:
                self[name] = PwData(name, size_val, alg=algo)

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
        manifestpath = os.path.join(PATH, "Data/manifest.json")
        with open(manifestpath, 'r') as m:
            manifest = json.load(m)
        try:
            match manifest:
                case {"passwords": name} if name == arg:
                    name = arg
                    filepath = os.path.join(PATH, "Data/", arg)
                case {"aliases": alias} if alias == arg:
                    name = manifest["aliases"][alias]["references"]
                    filepath = os.path.join(PATH, "Data/", name)
                case _:
                    raise (KeyError)
            os.remove(filepath)
        except Exception as e:
            if e is KeyError:
                print("Error {err} encountered looking for {item} in manifest."
                      .format(err=e, item=arg))
            else:
                print("Error {err} encountered deleting {item}"
                      .format(err=e, item=arg))
        self.pop(name)
