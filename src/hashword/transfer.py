import os
import paramiko
import shutil
from .filesys import FileSys


def copy_files(path, tpath):
    for file in os.listdir(path):
        if not file.endswith(('.json', '.bak', '.transfer')):
            filepath = os.path.join(path, file)
            newname = str(file, '.transfer')
            transferpath = os.path.join(tpath, newname)
            shutil.copyfile(filepath, transferpath)


def transfer(user, host):

    # p = FileSys()
    # temp = p.temp_dir()
    # copy_files(p.DATA_PATH, temp)
    client = paramiko.SSHClient()
    client.load_system_host_keys()

    client.connect(hostname=host,
                   username=user,
                   key_filename=None,
                   allow_agent=True,
                   look_for_keys=True)
    stdin, stdout, stderr = client.exec_command("ls")
    directory_list = stdout.read().decode().strip()
    print(directory_list)
