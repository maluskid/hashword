from hashword import helptext
from hashword.pwdata import PwData
from hashword.manifest import Manifest
from hashword.filesys import FileSys
from hashword.rsaencrypt import Encrypto
from hashword.transfer import transfer
from copy import deepcopy
from cryptography.fernet import InvalidToken
import os
import json


class HashWord(dict):

    def __init__(self):
        self.p = FileSys()
        self.p.create()

    def alias(self, target, nickname):
        manifest = Manifest()
        manifest.add_alias(target, nickname)
        manifest.close()

    def audit(self, rsapath=None):
        '''
        Iterates over entire manifest and every saved password to compare
        values. Orphaned passwords and aliases will be removed from the
        manifest, passwords which haven't been recorded in the manifest will
        be added. Any aliases which may have been assigned to an unrecorded
        password will need to be reset.
        '''
        manifest = Manifest()
        try:
            self.populate(rsapath)
        except InvalidToken:
            print(helptext.AUDIT_ENCRYPTION_DISCREPANCY)
            manifest.encrypted = False
            # If fernet.InvalidToken was raised, hashword is trying to decrypt
            # and failing. Possibly due to passwords being unencrypted.
            manifest.close()
            self.populate(rsapath)
            manifest = Manifest()
        except json.decoder.JSONDecodeError:
            print(helptext.AUDIT_ENCRYPTION_DISCREPANCY)
            manifest.encrypted = True
            # If JSONDecodeError was raised, hashword is trying to deserialize
            # a file which isn't deserializable. Possibly an encrypted file.
            manifest.close()
            self.populate()
            manifest = Manifest()
        if manifest.passwords or self:
            old = deepcopy(self)
            old_man = deepcopy(manifest)
            for item in old_man.passwords:
                print("Checking password", item)
                old.pop(item)
                if item not in self and item in manifest.passwords:
                    print(item, "is an orphaned password...")
                    manifest.audit(item)
            for key, val in old_man.aliases.items():
                print("Checking alias", key, "of", val)
                if val not in self and key in manifest.aliases:
                    print(key, "is an orphaned alias...")
                    manifest.audit(key)
            for key in old:
                print("Ensuring manifest entry for", key)
                if key not in manifest.passwords:
                    print(key, "not recorded.")
                    manifest.add_pw(key)
                    print("Entry for", key, "added to manifest.")
        else:
            print("Nothing to audit.")
        manifest.close()

    def create(self, algo, name, seed, size, rsapath=None):
        data = {'algo': algo, 'name': name, 'seed': seed, 'size': size}
        match [size, algo]:
            case [size_val, ('blake2b' | 'sha256')]:
                if not size_val or size_val > 64:
                    data['size'] = 64
            case [size_val, ('md5' | 'sha-3')]:
                if not size_val or size_val > 32:
                    data['size'] = 32
            case [size_val, _]:
                data['algo'] = 'sha256'
                if not size_val or size_val > 64:
                    data['size'] = 64
        match seed:
            case None:
                self[name] = PwData(data)
            case seed_val if len(seed_val) > 4:
                seed_val += '\n'
                data['seed'] = seed_val
                self[name] = PwData(data)
            case seed_val if len(seed_val) <= 4:
                raise (ValueError("""Seed must be at least 5 characters in
                    length. Creating a password without a seed will default to
                    a randomly generated one."""))
        self.save(rsapath)

    def delete(self, arg):
        manifest = Manifest()
        try:
            targ = manifest.rm_pw(arg)
        except ValueError as e:
            helptext.print_error(e)
            helptext.print_usage(True)
        else:
            filepath = os.path.join(self.p.DATA_PATH, targ)
            os.remove(filepath)
            manifest.close()

    def get(self, target, rsapath):
        manifest = Manifest()
        if target in manifest.passwords:
            name = target
            self.load(name, rsapath)
            return (self[name].getpw())
        elif target in manifest.aliases:
            name = manifest.aliases[target]
            self.load(name, rsapath)
            return (self[name].getpw())
        else:
            print("""Value not found in manifest. Use the `audit` command to
            help fix a broken manifest.""")

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
        if manifest.encrypted:
            print("\nPasswords are encrypted.")
        else:
            print("\nPasswords not encrypted.")
        print('\n', end='')

    def load(self, name, rsapath):
        # loads a specific password
        filepath = os.path.join(self.p.DATA_PATH, name)
        manifest = Manifest()
        e = None
        if manifest.encrypted and rsapath:
            e = Encrypto(rsapath)
        elif manifest.encrypted:
            print("No key path provided, looking in .hashword/Keys directory.")
            e = Encrypto(self.p.PRIV_KEY_PATH)
        item = None
        with open(filepath, 'rb') as f:
            if e:
                encitem = f.read()
                item = json.loads(e.decrypt(encitem))
            else:
                item = json.load(f)
        if item:
            self[name] = PwData(item)

    def populate(self, rsapath=None):
        # loads every saved password in one go
        e = None
        manifest = Manifest()
        encitems = dict()
        if manifest.encrypted and rsapath:
            e = Encrypto(rsapath)
        elif manifest.encrypted:
            print("No key path provided, looking in .hashword/Keys directory.")
            e = Encrypto(self.p.PRIV_KEY_PATH)

        for file in os.listdir(self.p.DATA_PATH):
            if not file.endswith(('.json', '.bak', '.transfer')):
                filepath = os.path.join(self.p.DATA_PATH, file)
                decitem = None
                with open(filepath, 'rb') as f:
                    if manifest.encrypted:
                        encitems[file] = f.read()
                    else:
                        decitem = json.load(f)
                        self[file] = PwData(decitem)
        if manifest.encrypted:
            decitems = e.mass_decrypt(encitems)
            for key in decitems:
                item = json.loads(decitems[key])
                self[key] = PwData(item)

    def rsa_setup(self, force, verbose):
        self.populate()
        e = Encrypto()
        e.setup(force_overwrite=force, verbose=verbose)
        # path to private rsa key should be constant unless user is
        # deleting files while Hashword is running.
        self.save(self.p.PRIV_KEY_PATH)

    def rsa_toggle(self, rsapath):
        manifest = Manifest()
        self.populate(rsapath)
        if manifest.encrypted:
            print("Unencrypting passwords...")
            manifest.encrypted = False
        else:
            print("Encrypting passwords...")
            manifest.encrypted = True
        manifest.close()
        self.save(rsapath)

    def save(self, rsapath=None):
        dirpath = self.p.DATA_PATH
        manifest = Manifest()
        e = None
        if manifest.encrypted and rsapath:
            e = Encrypto(rsapath)
        elif manifest.encrypted:
            print("No key path provided, looking in .hashword/Keys directory.")
            e = Encrypto(self.p.PRIV_KEY_PATH)

        if e:
            items = dict()
            for key in self:
                if self[key].name not in manifest.passwords:
                    manifest.add_pw(self[key].name)
                items[self[key].name] = json.dumps({
                    'algo': self[key].hash_alg,
                    'name': self[key].name,
                    'seed': self[key].seed,
                    'size': self[key].size
                }).encode()
            encitems = e.mass_encrypt(items)
            for key in encitems:
                filepath = os.path.join(dirpath, key)
                with open(filepath, 'wb') as f:
                    f.write(encitems[key])
        else:
            for key in self:
                filepath = os.path.join(dirpath, self[key].name)
                if self[key].name not in manifest.passwords:
                    manifest.add_pw(self[key].name)
                item = {
                    'algo': self[key].hash_alg,
                    'name': self[key].name,
                    'seed': self[key].seed,
                    'size': self[key].size
                }
                with open(filepath, 'wb') as f:
                    f.write(json.dumps(item).encode())
        manifest.close()

    def showpath(self):
        return self.p.DATA_PATH

    def connect(self, user, host):
        transfer(user, host)
