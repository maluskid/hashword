import os
import paramiko
import shutil
from hashword.filesys import FileSys


def get_remote_home_directory(ssh_client):
    commands = ["echo $HOME", "echo %USERPROFILE%", "pwd"]
    for command in commands:
        try:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            home_dir = stdout.read().decode().strip()
            if home_dir:
                return home_dir
        except Exception as e:
            print(f"Error executing command '{command}': {e}")
    return None


def copy_local_files(path, tpath):
    for file in os.listdir(path):
        if not file.endswith(('.json', '.bak', '.transfer')):
            filepath = os.path.join(path, file)
            newname = str(file + '.transfer')
            transferpath = os.path.join(tpath, newname)
            shutil.copyfile(filepath, transferpath)


def ensure_remote_dir(path, sftp):

    # Was having issues with directories being made without making the entire
    # path individually. Perhaps it has something to do with using the try
    # block as the logic check for if file exists
    tpath = os.path.join(path, '.hashword')
    try:
        sftp.mkdir(tpath)
    except IOError as e:
        # errno 17 == directory exists
        if e.errno == 17:
            pass
        else:
            print(f"Err sftp: {e}")
    except Exception as e:
        print(f"Err sftp: {e}")

    # Once home/.hashword/ directory is ensured, create ../.hashword/Transfer/
    tpath = os.path.join(tpath, 'Transfer')
    try:
        sftp.mkdir(tpath)
    except IOError as e:
        if e.errno == 17:
            pass
        else:
            print(f"Err sftp: {e}")
    except Exception as e:
        print(f"Err sftp: {e}")

    return tpath


def sftp_transfer(path, tpath, sftp):
    for file in os.listdir(path):
        if file.endswith('.transfer'):
            try:
                filepath = os.path.join(path, file)
                transferpath = os.path.join(tpath, file)
                sftp.put(filepath, transferpath)
            except Exception as e:
                print(f"Err sftp: {e}")
    sftp.close()


def transfer(user, host):
    p = FileSys()
    temp = p.temp_dir()
    copy_local_files(p.DATA_PATH, temp)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    print(f"Connecting to {user}@{host}...")
    client.connect(hostname=host,
                   username=user,
                   key_filename=None,
                   allow_agent=True,
                   look_for_keys=True)
    remotehome = get_remote_home_directory(client)
    print(f"Remote home dir: {remotehome}")
    sftp = client.open_sftp()
    remotetarget = ensure_remote_dir(remotehome, sftp)
    sftp_transfer(temp, remotetarget, sftp)
    client.close()
    shutil.rmtree(temp)
