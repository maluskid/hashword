import getpass
import hashlib
import os
import pickle
import random
import rsa


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


USER = getpass.getuser().strip()
PATH = "/home/" + USER + "/.hashword/Data/"
os.makedirs(PATH, exist_ok=True)


class HashWord(dict):

    def populate(self):
        for file in os.listdir(PATH):
            filepath = PATH + file
            with open(filepath, 'rb') as f:

                item = pickle.load(f)
                self[item.name] = item

    def save(self):
        for key in self:
            filepath = PATH + self[key].name
            with open(filepath, 'wb') as f:
                pickle.dump(self[key], f)

    def create(self):
        name = input("Enter a name for new passcode:\n")
        size = int(input("What is the max character" +
                         "count for this password?\n"))
        algo = input("Choose a hashing algorithm:\n\t1) sha256" +
                     "\n\t2) md5\n\t3) sha-3\n\t4) blake2b\n")
        seed = input("Choose a seed to create your password" +
                     "with or press Enter:\n").strip()
        match algo:
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

    def delete(self, name):
        filepath = os.path.join(PATH, name)
        try:
            os.remove(filepath)
        except OSError as e:
            print(e, "Encountered deleting")
        self.pop(name)
