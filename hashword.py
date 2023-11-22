#! /bin/python3
import hashlib, os, pickle, random

def seed_generator():
    alphabet = ['0','1','2','3','4','5','6','7','8',
                '9','a','b','c','d','e','f','g','h',
                'i','j','k','l','m','n','o','p','q',
                'r','s','t','u','v','w','x','y','z'] 
    random.seed()
    out = ''
    for i in range(24):
        index = random.randrange(36)
        out += alphabet[index]
    return out
   
class PwData:

    def __init__(self, name, size, alg=None, seed=seed_generator(), alias=list()):
        self.name = name
        self.size = size
        self.hash_alg = alg
        self.seed = seed
        if type(alias_list) is not list:
            raise(TypeError("Aliases must be formatted as a list"))
        self.alias_list=alias

    def add_alias(self, alias):
        self.alias_list.append(alias)

    def getpw(self):
        h = None
        match self.hash_alg:
            case 'shake256':
                h = hashlib.shake_256()
            case 'blake2b':
                h = hashlib.blake2b()
            case 'md5':
                h = hashlib.md5()
            case _:
                h = hashlib.sha256()

        h.update(self.seed.encode())
        temp = h.hexdigest()
        print(temp)
        out = ''
        for i in range(self.size):
            out += temp[i]  

        return out

class HashWord(dict):
    
    def populate(self):
        for file in os.listdir('./Data/'):
            with open(os.fsdecode(file), 'r') as f:
                item = pickle.load(f)
                self[item.name] = item

    def save(self):
        for key in self:
            path = './Data/' + self[key].name
            with open(path, mode='wb') as f:
                pickle.dump(self[key], f)
    
    def create(self):
        name = input("Enter a name for new passcode:")
        size = int(input("What is the max character count for this password?"))
        algo = input("Choose a hashing algorithm:\n\t1) sha256\n\t2) md5\n\t3) shake256\n\t4) blake2b")
        seed = input("Choose a seed to create your password with or press Enter:")
        match algo:
            case '2':
                if len(seed) > 0:
                    self[name] = PwData(name, size, seed=seed, hash_alg='md5')
                else:
                    self[name] = PwData(name, size, hash_alg='md5')
            case '3':
                if len(seed) > 0:
                    self[name] = PwData(name, size, seed=seed, hash_alg='shake256')
                else:
                    self[name] = PwData(name, size, hash_alg='shake256')
            case '4':
                if len(seed) > 0:
                    self[name] = PwData(name, size, seed=seed, hash_alg='blake2b')
                else:
                    self[name] = PwData(name, size, hash_alg='blake2b')
            case _:
                if len(seed) > 0:
                    self[name] = PwData(name, size, seed=seed, hash_alg='sha256')
                else:
                    self[name] = PwData(name, size, hash_alg='sha256')

    def add(self):
        c = input("Would you like to add a password? (y/n)")
        while(c != 'n' or c != 'N'):
            if c == 'y' or c == 'Y':
                self.create()             
            else:
                print("Please enter (y/n)")

    def list(self):
        count = 0
        for key in self:
            count += 1
            print(count, "\t", key)

if __name__ == "__main__":
    h = HashWord()
    match sys.argv[1]:
        case 'add':
            h.add()
        case 'list':
            h.list()
        case _:
            if sys.argv[1] 
            print("Usage:\n\tadd\n\tlist\n\t<name of password>")
