import os
import json
from . import helptext
from .filesys import FileSys


class Manifest():

    def __init__(self):
        self.p = FileSys()
        self.passwords = list()
        self.aliases = dict()
        if os.path.getsize(self.p.M_PATH) > 0:
            with open(self.p.M_PATH, 'r+') as m:
                try:
                    savedm = json.load(m)
                    self.aliases.update(savedm["aliases"])
                    self.passwords = savedm["passwords"].copy()
                except json.JSONDecodeError as e:
                    print("Error: {err} encountered decoding manifest.json"
                          .format(err=e))
        elif os.path.getsize(self.p.DATA_PATH) > 5:
            # If DATA_PATH is empty or nearly empty, it is likely there are no
            # saved passwords and the warning is unneccessary
            print(helptext.WARN_MANIFEST)

    def close(self):
        with open(self.p.M_PATH, 'w+') as m:
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
            print("Alias", alias, "for", pw, "removed.")

    def add_pw(self, password):
        if password not in self.passwords:
            self.passwords.append(password)
        else:
            raise (ValueError("Element already exists in list."))

    def print(self):
        print("Passwords:\n")
        for p in self.passwords:
            print(p)
        print("Aliases:\n")
        for k, v in self.aliases.items():
            print(k, " --> ", v)

    def rm_pw(self, target):

        match target:
            case al if al in self.aliases:
                pw = self.aliases[al]
                self.rm_alias(al, True)
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
        '''
        Function to find and delete orphaned items from manifest
        The target variable can be any password name or alias. Raises a
        ValueError if target is invalid.
        '''
        match target:
            case al if al in self.aliases:
                self.aliases.pop(al)
                print("Orphaned alias removed.")
            case pw if pw in self.passwords:
                self.passwords.remove(pw)
                print("Orphaned password removed.")
                print("Checking for aliases of", pw)
                keylist = []
                if pw in self.aliases.values():
                    for key in self.aliases.keys():
                        if self.aliases[key] == pw:
                            keylist.append(key)
                if keylist:
                    print("Removing aliases:")
                    for a in keylist:
                        print(a)
                        self.aliases.pop(a)
            case _:
                raise (ValueError("Element not in list."))
