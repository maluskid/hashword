import os
import json
from hashword import helptext
from hashword.filesys import FileSys


class Manifest:

    def __init__(self):
        self.p = FileSys()
        self.passwords = list()
        self.aliases = dict()
        self.encrypted = False
        self.load_self()

    def close(self):
        '''Saves the current values in manifest object to the
        data directory.'''
        with open(self.p.M_PATH, 'w+') as m:
            msaver = {
                "passwords": self.passwords,
                "aliases": self.aliases
            }
            json.dump(msaver, m)

    def load_self(self):
        '''
        Function which checks if a manifest exists and creates a new blank one
        if it doesn't. If it does exist, it will attempt to load the data in
        the manifest. If an error occurs, it will prompt user to run the
        `audit` command and create a new blank manifest.
        '''
        if os.path.exists(self.p.M_PATH):
            if os.stat(self.p.M_PATH).st_size > 0:
                try:
                    with open(self.p.M_PATH, 'r+') as m:
                        savedm = json.load(m)
                    self.aliases.update(savedm["aliases"])
                    self.passwords = savedm["passwords"].copy()
                    self.encrypted = savedm["encrypted"]
                except json.decoder.JSONDecodeError:
                    print(helptext.WARN_MANIFEST_LOAD)
                    os.remove(self.p.M_PATH)
                    self.close()
            else:
                with os.scandir(self.p.DATA_PATH) as data:
                    # Only print warning if there are files
                    if any(data):
                        print(helptext.WARN_MANIFEST_EMPTY)
                self.close()
        else:
            with os.scandir(self.p.DATA_PATH) as data:
                # Only print warning if there are files
                if any(data):
                    print(helptext.WARN_MANIFEST_EXISTS)
            self.close()

    def add_alias(self, target, alias):
        if target in self.passwords:
            self.aliases[alias] = target
        else:
            raise (ValueError("Element not in list."))

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
