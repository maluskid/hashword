from cryptography.fernet import Fernet
import os
import pickle
import rsa
import sys
import getpass
from . import helptext
from .filesys import FileSys

# If for some reason you want this program to generate RSA keys of a different
# length, change that here.
KEY_LEN = 3072


class Encrypto():

    def __init__(self):
        self.user = getpass.getuser()
        self.p = FileSys()

    def load(self):
        if os.path.getsize(self.p.KEY_PATH) > 0 and self.user:
            with open(os.path.join(self.p.KEY_PATH, self.user), 'rb') as f:
                self.pubkey = rsa.PublicKey.load_pkcs1((pickle.load(f)))
        elif os.path.getsize(self.p.KEY_PATH < 5):
            # If no files saved in key_path, encryption hasn't been set up.
            print(helptext.WARN_KEYS)
        else:
            raise (FileNotFoundError)

    def setup(self, verbose=False):
        print(helptext.RSA_SETUP0)
        privpath = input("\n\tEnter path to the location at which you would" +
                         "like to save your\n\tprivate key:")
        [pub, priv] = rsa.newkeys(KEY_LEN)
        if verbose:
            print("Your private key:\n\n", priv.save_pkcs1().decode())
        try:
            with open(privpath, 'wb') as p:
                pickle.dump(priv.save_pkcs1(), p)
            with open(os.path.join(self.p.KEY_PATH, self.user), 'wb') as f:
                pickle.dump(pub.save_pkcs1(), f)
        except Exception as e:
            print("Error {err} This occurred while saving keys, exiting."
                  .format(err=e))
            sys.exit(1)
