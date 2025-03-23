import os
import rsa
from cryptography.fernet import Fernet
from hashword import helptext
from hashword.filesys import FileSys
from hashword.manifest import Manifest

# If for some reason you want this program to generate RSA keys of a different
# length, change that here.
KEY_LEN = 3072


class Encrypto:

    def __init__(self, key=None):
        self.p = FileSys()
        if key:
            self.privkey = self.load_privkey(key)
        else:
            self.privkey = None

    def load_fkey(self):
        fernet = None
        if os.path.exists(self.p.FERNET):
            with open(self.p.FERNET, 'rb') as f:
                enc_fkey = f.read()
                fkey = rsa.decrypt(enc_fkey, self.privkey)
                fernet = Fernet(fkey)
        return fernet

    def load_privkey(self, keypath):
        if os.path.exists(keypath):
            with open(keypath, 'rb') as f:
                return rsa.PrivateKey.load_pkcs1(f.read())
        else:
            raise (FileNotFoundError)

    def setup(self, force_overwrite=False, verbose=False):
        print(helptext.RSA_SETUP0)
        [pub, priv] = rsa.newkeys(KEY_LEN)
        self.privkey = priv
        fkey = Fernet.generate_key()

        if verbose:
            print("Your private key:\n\n", priv.save_pkcs1().decode())
            input("\n\nPress any key to show your public key...")
            print("\n\nYour public key:\n\n", pub.save_pkcs1().decode())

        m = Manifest()
        ok = m.add_encryption(force_overwrite)
        m.close()
        if ok:
            with open(self.p.PRIV_KEY_PATH, 'wb') as p:
                p.write(priv.save_pkcs1())
            with open(self.p.PUB_KEY_PATH, 'wb') as p:
                p.write(pub.save_pkcs1())
            with open(self.p.FERNET, 'wb') as f:
                encryptedfkey = rsa.encrypt(fkey, pub)
                f.write(encryptedfkey)
            print(helptext.RSA_SETUP1)

    def mass_encrypt(self, targets):
        out = dict()
        fernet = self.load_fkey()
        for key in targets:
            out[key] = fernet.encrypt(targets[key])
        return out

    def encrypt(self, target):
        fernet = self.load_fkey()
        return fernet.encrypt(target)

    def mass_decrypt(self, targets):
        out = dict()
        fernet = self.load_fkey()
        for key in targets:
            dec = fernet.decrypt(targets[key])
            out[key] = dec
        return out

    def decrypt(self, target):
        fernet = self.load_fkey()
        return fernet.decrypt(target)
