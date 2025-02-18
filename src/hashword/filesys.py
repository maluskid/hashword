import getpass
import os

user = getpass.getuser().strip()
path = os.path.join('/home', user, '.hashword/')
keypath = os.path.join(path, 'Keys/')


class FileSys:

    def __init__(self):
        # Main data path
        # self.DATA_PATH = os.path.join(path, 'Data/')
        # Alternate testing data path
        self.DATA_PATH = os.path.join(path, 'Testing/')
        self.PRIV_KEY_PATH = os.path.join(path, 'Keys/', 'hashword_key_priv')
        self.PUB_KEY_PATH = os.path.join(path, 'Keys/', 'hashword_key_pub')
        self.M_PATH = os.path.join(self.DATA_PATH, 'manifest.json')
        self.FERNET = os.path.join(path, 'Keys/', user)
        # create relevant directories and files if they don't exist
        if not os.path.exists(self.DATA_PATH):
            os.makedirs(os.path.join(self.DATA_PATH))
        if not os.path.exists(keypath):
            os.makedirs(os.path.join(keypath))
        if not os.path.exists(self.M_PATH):
            with open(self.M_PATH, 'x'):
                print("""
                `manifest.json` not found, starting fresh. Use the `audit`
                command to help fix a broken manifest. If this is the first
                time you've used hashword, you can ignore this message.'
                """)
