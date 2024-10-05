import os
import pickle
import rsa
import sys
import getpass
from cryptography.fernet import Fernet
from . import helptext
from .filesys import FileSys
from .manifest import Manifest

# If for some reason you want this program to generate RSA keys of a different
# length, change that here.
KEY_LEN = 3072


class Encrypto():

    def __init__(self, key=None):
        self.user = getpass.getuser()
        self.p = FileSys()
        if key:
            self.privkey = self.load_privkey(key)

    def load_fkey(self):
        fernet = None
        try:
            if os.path.getsize(self.p.KEY_PATH) > 0 and self.user:
                with open(os.path.join(self.p.KEY_PATH, self.user), 'rb') as f:
                    enc_fkey = f.read()
                    fkey = rsa.decrypt(enc_fkey, self.privkey)
                    fernet = Fernet(fkey)
            elif os.path.getsize(self.p.KEY_PATH < 5):
                # If no files saved in key_path, encryption hasn't been set up.
                print(helptext.WARN_KEYS)
            else:
                raise (FileNotFoundError)
        except Exception as e:
            helptext.print_error(e)
        return fernet

    def load_privkey(keypath):
        if os.path.exists(keypath):
            with open(keypath, 'rb') as f:
                return rsa.PrivateKey.load_pkcs1(f)
        else:
            raise (FileNotFoundError)

    def setup(self, force_overwrite=False, verbose=False):
        print(helptext.RSA_SETUP0)
        os.system("PAUSE")
        [pub, priv] = rsa.newkeys(KEY_LEN)
        self.privkey = priv
        fkey = Fernet.generate_key()

        if verbose:
            print("Your private key:\n\n", priv.save_pkcs1().decode())
            input("\n\nPress any key to show your public key...")
            print("\n\nYour public key:\n\n", pub.save_pkcs1().decode())
        try:
            manifest = Manifest()
            [ok, needs_encrypt] = manifest.add_encryption(force_overwrite)
            manifest.close()
            if ok:
                with open("rsa_key_priv", 'wb') as p:
                    p.write(priv.save_pkcs1())
                with open("rsa_key_pub", 'wb') as p:
                    p.write(pub.save_pkcs1())
                with open(os.path.join(self.p.KEY_PATH, self.user), 'wb') as f:
                    encryptedfkey = rsa.encrypt(fkey, pub)
                    f.write(encryptedfkey)
                print(helptext.RSA_SETUP1)
            return needs_encrypt
        except Exception as e:
            print("Error: {err} This occurred while saving keys, exiting."
                  .format(err=e))
            sys.exit(1)

    def mass_encrypt(self, data):
        ret = dict()
        current = ''
        try:
            fernet = self.load_fkey()
            for key in data:
                current = key
                ret[key] = fernet.encrypt(data[key])
        except Exception as e:
            helptext.print_error(e)
            print("This occurred while encrypting {k}, exiting."
                  .format(k=current))
            sys.exit(1)
        return ret

    def mass_decrypt(self, data):
        ret = dict()
        current = ''
        try:
            fernet = self.load_fkey()
            for key in data:
                current = key
                ret[key] = fernet.decrypt(data[key])
        except Exception as e:
            helptext.print_error(e)
            print("This occurred while decrypting {k}, exiting."
                  .format(k=current))
            sys.exit(1)
        return ret

    def encrypt(self, target):
        try:
            fernet = self.load_fkey()
            return fernet.encrypt(target)
        except Exception as e:
            print(
                "Error: {err} This occurred while encrypting {t}, exiting."
                .format(err=e, t=target))
            sys.exit(1)

    def decrypt(self, target):
        try:
            fernet = self.load_fkey()
            return fernet.decrypt(target)
        except Exception as e:
            print(
                "Error: {err} This occurred while decrypting {t}, exiting."
                .format(err=e, t=target))
            sys.exit(1)
