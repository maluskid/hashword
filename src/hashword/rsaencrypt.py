import os
import rsa
import sys
from cryptography.fernet import Fernet
from . import helptext
from .filesys import FileSys
from .manifest import Manifest

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
        try:
            if os.path.getsize(self.p.FERNET) > 2:
                with open(self.p.FERNET, 'rb') as f:
                    enc_fkey = f.read()
                    fkey = rsa.decrypt(enc_fkey, self.privkey)
                    fernet = Fernet(fkey)
        except Exception as e:
            helptext.print_error(e)
            # If no files saved in key_path, encryption hasn't been set up.
            print(helptext.WARN_KEYS)
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
        # try:
        m = Manifest()
        ok = m.add_encryption(force_overwrite)
        m.close()
        if ok:
            with open("hashword_key_priv", 'wb') as p:
                p.write(priv.save_pkcs1())
            with open("hashword_key_pub", 'wb') as p:
                p.write(pub.save_pkcs1())
            with open(self.p.FERNET, 'wb') as f:
                encryptedfkey = rsa.encrypt(fkey, pub)
                f.write(encryptedfkey)
            print(helptext.RSA_SETUP1)
        # except Exception as e:
        #     print("Error: {err} This occurred while saving keys, exiting."
        #           .format(err=e))
        #     sys.exit(1)

    def mass_encrypt(self, targets):
        out = dict()
        fernet = self.load_fkey()
        for key in targets:
            out[key] = fernet.encrypt(targets[key])
        return out

    def encrypt(self, target):
        try:
            fernet = self.load_fkey()
            return fernet.encrypt(target)
        except Exception as e:
            print(
                "Error: {err} This occurred while encrypting {t}, exiting."
                .format(err=e, t=target))
            sys.exit(1)

    def mass_decrypt(self, targets):
        out = dict()
        fernet = self.load_fkey()
        for key in targets:
            out[key] = fernet.decrypt(targets[key])
        return out

    def decrypt(self, target):
        try:
            fernet = self.load_fkey()
            return fernet.decrypt(target)
        except Exception as e:
            print(
                "Error: {err} This occurred while decrypting {t}, exiting."
                .format(err=e, t=target))
            sys.exit(1)

    def undo(self):
        m = Manifest()
        m.encrypted = False
        m.close()
        os.remove('./hashword_key_pub')
        os.remove('./hashword_key_priv')
        os.remove(self.p.FERNET)
