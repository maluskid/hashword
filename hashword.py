from cryptography.fernet import Fernet
import base64
import getpass
import hashlib
import helptext
import os
import pickle
import random
import rsa
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
        self.hash_alg = alg
        self.name = name
        self.seed = seed
        self.size = size

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


user = getpass.getuser().strip()
path = os.path.join('/home', user, '.hashword/')
DATA_PATH = os.path.join(path, 'Data/')
KEY_PATH = os.path.join(path, 'Keys/')
M_PATH = os.path.join(DATA_PATH, 'manifest.json')
# create relevant directories and files if they don't exist
if not os.path.exists(DATA_PATH):
    os.makedirs(os.path.join(DATA_PATH))
if not os.path.exists(KEY_PATH):
    os.makedirs(os.path.join(KEY_PATH))
if not os.path.exists(M_PATH):
    with open(M_PATH, 'x'):
        print("manifest.json not found, starting fresh.")


class Manifest():

    def __init__(self):
        self.passwords = list()
        self.aliases = dict()
        if os.path.getsize(M_PATH) > 0:
            with open(M_PATH, 'r+') as m:

                try:
                    savedm = json.load(m)
                    self.aliases.update(savedm["aliases"])
                    self.passwords = savedm["passwords"].copy()
                except json.JSONDecodeError as e:
                    helptext.print_error(e)
        elif os.path.getsize(DATA_PATH) > 5:
            # If DATA_PATH is empty or nearly empty, it is likely there are no
            # saved passwords and the warning is unneccessary
            print("WARN: manifest.json is empty. You may need to restore it.")

    def close(self):
        with open(M_PATH, 'w+') as m:
            msaver = {
                "passwords": self.passwords,
                "aliases": self.aliases
            }
            json.dump(msaver, m)

    def add_alias(self, target, alias):
        if target in self.passwords:
            self.aliases[alias] = target
        else:
            raise (ValueError("Target password not in list."))

    def rm_alias(self, alias, verbose=False):
        pw = self.aliases.pop(alias)
        if verbose:
            print("Alias {a} for {p} removed.".format(a=alias, p=pw))

    def add_pw(self, password):
        if password not in self.passwords:
            self.passwords.append(password)
        else:
            raise (ValueError("Element already exists in list."))

    def rm_pw(self, target):

        match target:
            case al if al in self.aliases:
                pw = self.aliases[al]
                self.rm_alias(pw, True)
                return self.rm_pw(pw)
            case pw if pw in self.passwords:
                self.passwords.remove(pw)
                if pw in self.aliases.values():
                    keylist = []
                    for key in self.aliases:
                        if self.aliases[key] == pw:
                            keylist.append(key)
                    if keylist:
                        for a in keylist:
                            self.rm_alias(a, True)
                return pw
            case _:
                raise (ValueError("Element not in list."))

    def audit(self, target):

        match target:
            case al if al in self.aliases:
                pw = self.aliases[al]
                self.aliases.pop(al)
                self.audit(pw)
            case pw if pw in self.passwords:
                self.passwords.remove(pw)
                if pw in self.aliases.values():
                    keylist = []
                    for key in self.aliases:
                        if self.aliases[key] == pw:
                            keylist.append(key)
                    if keylist:
                        for a in keylist:
                            self.aliases.pop(a)
                return pw
            case _:
                raise (ValueError("Element not in list."))


class HashWord(dict):

    def populate(self):
        # loads every saved password in one go
        for file in os.listdir(DATA_PATH):
            if not file.endswith('.json') and not file.endswith('.bak'):
                filepath = os.path.join(DATA_PATH, file)
                with open(filepath, 'rb') as f:
                    item = pickle.load(f)
                    self[item.name] = item

    def load(self, name):
        # loads a specific password
        filepath = os.path.join(DATA_PATH, name)
        with open(filepath, 'rb') as f:
            item = pickle.load(f)
            self[item.name] = item

    def save(self):
        dirpath = os.path.join(DATA_PATH)
        manifest = Manifest()
        for key in self:
            filepath = os.path.join(dirpath, self[key].name)
            manifest.add_pw(self[key].name)
            with open(filepath, 'wb') as f:
                pickle.dump(self[key], f)
        manifest.close()

    def get(self, target):
        try:
            manifest = Manifest()
            if target in manifest.passwords:
                name = target
            elif target in manifest.aliases:
                name = manifest.aliases[target]
            else:
                raise ValueError("Value not found in manifest.")
        except Exception as e:
            helptext.print_error(e)
        else:
            self.load(name)
            return (self[name])

    def create(self, algo, name, seed, size):
        match [size, algo]:
            case [size_val, ('blake2b' | 'sha256')]:
                if not size_val or size_val > 64:
                    size_val = 64
            case [size_val, ('md5' | 'sha-3')]:
                if not size_val or size_val > 32:
                    size_val = 32
            case [size_val, _]:
                algo = 'sha256'
                if not size_val or size_val > 64:
                    size_val = 64
        match seed:
            case None:
                self[name] = PwData(name, size_val, alg=algo)
            case seed_val if len(seed_val) > 4:
                seed_val += '\n'
                self[name] = PwData(name, size_val, seed=seed_val, alg=algo)
            case seed_val if len(seed_val) <= 4:
                raise (ValueError("Seed must be at least 5 characters in \
                    length. Creating a password without a seed will default \
                    to a randomly generated one."))
        self.save()

    def list_self(self):
        manifest = Manifest()
        count = 0
        print("\nPasswords:")
        for p in manifest.passwords:
            count += 1
            print(" {c})\t{item}".format(c=count, item=p))
        print('\n', end='')
        if len(manifest.aliases):
            print("Aliases:")
            for a in manifest.aliases:
                print("\t{alias}  -->  {pw}"
                      .format(alias=a, pw=manifest.aliases[a]))
        print('\n', end='')

    def alias(self, target, nickname):
        manifest = Manifest()
        manifest.add_alias(target, nickname)
        manifest.close()

    def delete(self, arg):
        manifest = Manifest()
        try:
            targ = manifest.rm_pw(arg)
        except ValueError as e:
            helptext.print_error(e)
            helptext.print_usage(True)
        except Exception as e:
            helptext.print_error(e)
        else:
            filepath = os.path.join(DATA_PATH, targ)
            try:
                os.remove(filepath)
                manifest.close()
            except Exception as e:
                helptext.print_error(e)

    def audit(self):
        manifest = Manifest()
        self.populate()
        for item in manifest.passwords:
            if item not in self.keys():
                print(item, manifest, "audit case0")
                manifest.audit(item)
        for val in manifest.aliases.values():
            if val not in self.keys():
                print(val, manifest, "audit case1")
                manifest.audit(val)
        manifest.close()
