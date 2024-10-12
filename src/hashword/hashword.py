from . import helptext
from .pwdata import PwData
from .manifest import Manifest
from .filesys import FileSys
from copy import deepcopy
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
        '''
        Iterates over entire manifest and every saved password to compare
        values. Orphaned passwords and aliases will be removed from the
        manifest, passwords which haven't been recorded in the manifest will
        be added. Any aliases which may have been assigned to an unrecorded
        password may need to be reset.
        '''
        manifest = Manifest()
        self.populate()
        old = deepcopy(self)
        old_man = deepcopy(manifest)
        for item in old_man.passwords:
            print("Checking password", item)
            if item not in self and item in manifest.passwords:
                print(item, "is an orphaned password...")
                manifest.audit(item)
        for key, val in old_man.aliases.items():
            print("Checking alias", key, "of", val)
            if val not in self and key in manifest.aliases:
                print(key, "is an orphaned alias...")
                manifest.audit(key)
        for key in old.keys():
            print("Ensuring manifest entry for", key)
            if key not in manifest.passwords:
                print(key, "not recorded.")
                manifest.add_pw(key)
                print("Entry for", key, "added to manifest.")
        manifest.close()

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
                raise (ValueError("""Seed must be at least 5 characters in
                    length. Creating a password without a seed will default to
                    a randomly generated one."""))
        self.save()

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

    def get(self, target):
        try:
            manifest = Manifest()
            if target in manifest.passwords:
                name = target
            elif target in manifest.aliases:
                name = manifest.aliases[target]
            else:
                raise ValueError("""Value not found in manifest. A broken
                password manifest can be fixed using the `audit` command.""")
        except Exception as e:
            helptext.print_error(e)
        self.load(name)
        return (self[name].getpw())

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
            for a, p in manifest.aliases.items():
                print("\t{alias}  -->  {pw}"
                      .format(alias=a, pw=p))
        print('\n', end='')

    def load(self, name):
        # loads a specific password
        try:
            filepath = os.path.join(self.p.DATA_PATH, name)
            with open(filepath, 'rb') as f:
                item = pickle.load(f)
                self[item.name] = item
        except Exception as e:
            helptext.print_error(e)

    def populate(self):
        # loads every saved password in one go
        for file in os.listdir(self.p.DATA_PATH):
            if not file.endswith('.json') and not file.endswith('.bak'):
                filepath = os.path.join(self.p.DATA_PATH, file)
                with open(filepath, 'rb') as f:
                    self[file] = pickle.load(f)

    def save(self):
        dirpath = os.path.join(self.p.DATA_PATH)
        manifest = Manifest()
        for key in self:
            filepath = os.path.join(dirpath, self[key].name)
            manifest.add_pw(self[key].name)
            with open(filepath, 'wb') as f:
                pickle.dump(self[key], f)
        manifest.close()

    def showpath(self):
        return self.p.DATA_PATH
