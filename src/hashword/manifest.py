import os
import json
from . import helptext
from .filesys import FileSys


class Manifest:

    def __init__(self):
        self.p = FileSys()
        self.passwords = list()
        self.aliases = dict()
        self.encrypted = False
        if os.path.exists(self.p.FERNET):
            # If a Fernet key has been saved,
            # encryption has been set up.
            self.encrypted = True
        if os.path.exists(self.p.M_PATH):
            with open(self.p.M_PATH, 'r+') as m:
                savedm = json.load(m)
                self.aliases.update(savedm["aliases"])
                self.passwords = savedm["passwords"].copy()
                self.encrypted = savedm["encrypted"]
        elif not os.listdir(self.p.DATA_PATH):
            # If DATA_PATH is empty, it is likely there are no
            # saved passwords and the warning is unneccessary
            print(helptext.WARN_MANIFEST)

    def close(self):
        with open(self.p.M_PATH, 'w+') as m:
            msaver = {
                "encrypted": self.encrypted,
                "passwords": self.passwords,
                "aliases": self.aliases
            }
            json.dump(msaver, m)

    def add_alias(self, target, alias):
        if target in self.passwords:
            self.aliases[alias] = target
        else:
            raise (ValueError("Element not in list."))

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
                self.rm_alias(al)
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
                            self.rm_alias(a)
                return pw
            case _:
                raise (ValueError("Element not in list."))

    def add_encryption(self, force):
        if self.encrypted and not force:
            print(helptext.WARN_RSA_OVERWRITE)
            return False
        else:
            if force:
                print("Overwriting previous key, force flag was set.")
            self.encrypted = True
            return True

    def audit(self, target):
        '''
        Function to find and delete orphaned items from manifest
        and create entries for saved passwords lacking one. The target variable
        can be any password name or alias. Raises a ValueError if target is
        invalid.
        '''
        match target:
            case al if al in self.aliases:
                self.rm_alias(al, True)
            case pw if pw in self.passwords:
                self.passwords.remove(pw)
                print("Orphaned password removed...")
                print("Checking for aliases of", pw)
                keylist = []
                if pw in self.aliases.values():
                    for key in self.aliases:
                        if self.aliases[key] == pw:
                            keylist.append(key)
                if keylist:
                    print("Removing aliases:")
                    for a in keylist:
                        print(a)
                        self.rm_alias(a)
            case _:
                raise (ValueError("Element not in list."))
