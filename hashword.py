import getpass
import hashlib
import os
import pickle
import rsa
import stat
import sys
import './pw_data.py'

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
                     "\n\t2) md5\n\t3) sha128\n\t4) blake2b\n")
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
                        name, size, seed=seed + '\n', alg='sha128')
                else:
                    self[name] = PwData(name, size, alg='sha128')
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

    def list(self):
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


if __name__ == "__main__":
    h = HashWord()
    # TODO: only run populate if needed
    h.populate()
    try:
        match sys.argv[1]:
            case 'add':
                h.create()
            case 'list':
                h.list()
            case 'del':
                try:
                    if sys.argv[2] in h:
                        h.delete(sys.argv[2])
                    else:
                        for key in h:
                            if sys.argv[2] in h[key].alias_list:
                                h.delete(h[key])
                                break
                except Exception as e:
                    print("Error {err} encountered deleting".format(err=e))
                    print("Usage:\n\thashword add\n\thashword list" +
                          "\n\thashword <name of password>" +
                          "\n\thashword del <name of password>" +
                          "\n\thashword alias <name of password> <alias>")
            case 'alias':
                try:
                    if sys.argv[2] in h:
                        h[sys.argv[2]].add_alias(sys.argv[3])
                    else:
                        for key in h:
                            if sys.argv[2] in h[key].alias_list:
                                h[key].add_alias(sys.argv[3])
                                break
                except Exception as e:
                    print("Error {err} encountered deleting".format(err=e))
                    print("Usage:\n\thashword add\n\thashword list" +
                          "\n\thashword <name of password>" +
                          "\n\thashword del <name of password>" +
                          "\n\thashword alias <name of password> <alias>")
            case '--help':
                print("'--help':\n\thashword add\n\thashword list" +
                      "\n\thashword <name of password>" +
                      "\n\thashword del <name of password>" +
                      "\n\thashword alias <name of password> <alias>")

            case _:
                inlist = False
                if sys.argv[1] in h:
                    print(h[sys.argv[1]].getpw())
                    inlist = True
                else:
                    for key in h:
                        if sys.argv[1] in h[key].alias_list:
                            print(h[key].getpw())
                            inlist = True
                            break
                if not inlist:
                    print("'{name}' not found in list.".format(
                        name=sys.argv[1]))
    except Exception as e:
        print("Invalid argument. Input `hashword --help` to view usage information.")
    h.save()
