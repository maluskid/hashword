from . import helptext
from .pwdata import PwData
from .manifest import Manifest
from .filesys import FileSys
import os
import pickle


class HashWord(dict):

    def __init__(self):
        self.p = FileSys()

    def alias(self, target, nickname):
        manifest = Manifest()
        manifest.add_alias(target, nickname)
        manifest.close()

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
        for key in self:
            if key not in manifest.passwords:
                manifest.add_pw(key)
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
            filepath = os.path.join(self.p.DATA_PATH, targ)
            try:
                os.remove(filepath)
                manifest.close()
            except Exception as e:
                helptext.print_error(e)

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
                self[name] = PwData(algo=algo, name=name, size=size_val)
            case seed_val if len(seed_val) > 4:
                seed_val += '\n'
                self[name] = PwData(algo=algo, name=name,
                                    seed=seed_val, size=size_val)
            case seed_val if len(seed_val) <= 4:
                raise (ValueError("Seed must be at least 5 characters in \
                    length. Creating a password without a seed will default \
                    to a randomly generated one."))
        self.save()

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
            return (self[name].getpw())

    def load(self, name):
        # loads a specific password
        filepath = os.path.join(self.p.DATA_PATH, name)
        with open(filepath, 'rb') as f:
            item = pickle.load(f)
            self[item.name] = item

    def populate(self):
        # loads every saved password in one go
        for file in os.listdir(self.p.DATA_PATH):
            if not file.endswith('.json') and not file.endswith('.bak'):
                filepath = os.path.join(self.p.DATA_PATH, file)
                with open(filepath, 'rb') as f:
                    item = pickle.load(f)
                    self[item.name] = item

    def save(self):
        dirpath = os.path.join(self.p.DATA_PATH)
        manifest = Manifest()
        for key in self:
            filepath = os.path.join(dirpath, self[key].name)
            manifest.add_pw(self[key].name)
            with open(filepath, 'wb') as f:
                pickle.dump(self[key], f)
        manifest.close()

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
