import os
import getpass

USERNAME = getpass.getuser()
USER = os.path.expanduser('~')
PATH = os.path.join(USER, '.hashword')
KEYPATH = os.path.join(PATH, 'Keys')


class FileSys:

    def __init__(self):
        # Main data path
        self.DATA_PATH = os.path.join(PATH, 'Data')
        # Alternate testing data PATH
        # self.DATA_PATH = os.path.join(PATH, 'Testing')
        self.PRIV_KEY_PATH = os.path.join(KEYPATH, 'hashword_key_priv')
        self.PUB_KEY_PATH = os.path.join(KEYPATH, 'hashword_key_pub')
        self.SSH_PATH = os.path.join(KEYPATH, '.ssh')
        self.TRANSFER_PATH = os.path.join('.hashword', 'Transfer')
        self.M_PATH = os.path.join(self.DATA_PATH, '.manifest.json')
        self.FERNET = os.path.join(PATH, 'Keys', USERNAME)

    def create(self):
        # create relevant directories and files if they don't exist
        if not os.path.exists(self.DATA_PATH):
            os.makedirs((self.DATA_PATH))
        if not os.path.exists(KEYPATH):
            os.makedirs(KEYPATH)

    def temp_dir(self):
        temp_path = os.path.join(PATH, 'Temp')
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        return temp_path
