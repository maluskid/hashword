# Most of the text output for the various functions in hashword is stored here
# to reduce clutter and make consistent formatting easier.

# Important help text below ---------------------------------------------------
USAGE = """
Usage:
    hashword <command>

    hashword <foo>                  show hash for <foo>
    hashword add                    add new password
    hashword alias <foo> <alias>    alias <foo> as <alias>
    hashword audit                  audits saved aliases and passwords
    hashword data                   show path to `/.hashword/data`
    hashword list                   list saved passwords
    hashword rm <foo>               remove <foo>
    hashword rsa                    manage RSA keys
    hashword transfer               transfer passwords over ssh
"""

NO_ENTRY = """
There isn't a help entry written for that yet . If you have suggestions
for improving Hashword or find any issues, report them at: 
https://github.com/maluskid/hashword/issues.
"""

MAIN_TEXT = """
Usage:
    hashword <foo>

    Print the hash of the saved value corresponding to <foo> or any
    password <foo> is an alias of to STDOUT. Use `hashword list` to
    view stored passwords and aliases. All data is stored in the home
    directory. The path to this directory can be found with `hashword
    data` Use `hashword rm <foo>` to remove all data pertaining to
    <foo> from the data directory. This *CANNOT* be undone, so use
    caution when executing this command.

    Copying from the terminal to your clipboard is OS dependant,
    please consult the relevant documentation accordingly. Some common
    default commands are listed below:
    Windows Powershell - <ctrl-c>
    Gnome Terminal  - <ctrl-shift-c>
    Mac Terminal - <cmd-c>
"""

# Help entries in alphabetical order below ------------------------------------
ADD_TEXT = """
Usage: hashword add
    This command will begin a step by step process in the terminal to add a new
    password to the keyring. Multiple hashing algorithms are available to
    select from:
        sha256, blake2b, md5, sha-3
    If none is supplied, sha256 is the default. If desired, the user can supply
    a certain input to be the seed for the resultant hash. This allows the user
    to reproduce the same hashed password value across multiple computers all
    running hashword. If no seed is provided, a randomized seed is produced
    and kept hidden. This option provides maximum security, but makes it
    impossible to recreate the password if lost. Seeds are stored with the rest
    of a password's data in the files located in `../.hashword/data`. The full
    path to this directory can be viewed with the `data` command.
"""

ADD_FLAGS = """
Flags:

    -s <number> Determines the maximum size of the output, in the case
        of a password field which limits total size. A size of 30 is usually
        sufficient for most needs. If unentered, defaults to maximum size.
    -S <seed> Generates the hash for a password from the specified seed.
        Allows a user to recreate the same hash on multiple machines wihtout
        the need for the `transfer` command.
    -a <algorithm> Determines the hashing algorithm to be used generating
        a given password. Valid inputs are:
            'sha256', 'sha-3', 'blake2b', 'md5'
        If unentered, will default to sha256 hashing.

Formatting: hashword add <keys> <name>

    E.G. -- `hashword add -s 30 -S secretsalt -a blake2b test`
    This will generate a hash with a seed of 'secretsalt' using the blake2b
    algorithm named 'test'. It will only output the first 30 characters of the
    hash whenever called.
"""

ALIAS_TEXT = """
Usage: hashword alias <foo> <alias>

    This command will link the password <foo> to an alias <alias>. Any
    subsequent calls to hashword will treat any command using <alias> the same
    as though it were entered using <foo>. You can view all aliases with the
    `list` command.
"""

AUDIT_TEXT = """
Usage: hashword audit

    This command will perform an audit of the saved `manifest.json` and all
    saved passwords. Use this command if an old password isn't
    recognized after a fresh installation. Aliases previously assigned
    to an old password entry will be lost and must be reassigned. If a
    password file has been removed without the use of the `rm` command,
    this command will fix the broken manifest.
"""

AUDIT_ENCRYPTION_DISCREPANCY = """
Error attempting to load files. Manifest may have invalid encryption setting.
Toggling manifest and trying again.
"""

DATA_TEXT = """
Usage: hashword data

    This command will display path to the data directory where all password
    data is stored. If RSA encryption hasn't been set up, these files are
    incredibly easy to gain information from. For your data safety, using RSA
    encryption is highly recommended.
"""

LIST_TEXT = """
Usage: hashword list

    This command displays all saved passwords as well as any aliases assigned
    to them.
"""

RM_TEXT = """Usage: hashword rm <foo>
This command removes all files stored in the .hashword/data/ directory
pertaining to <foo>. This *CANNOT* be undone, so use care when executing this
command. Making a backup is recommended, all are named by the password they
refer to. Hashword encrypts all password files with your RSA public key before
saving them.
"""

RSA_TEXT = """
Usage: hashword rsa

    This software can use RSA keys to verify your identity and protect your
    passwords. The `rsa --setup` command will begin the encryption process if
    RSA encryption keys haven't previously been implemented. Passwords are
    encrypted using your public key. In order to decrypt them, you must supply
    your private key. The first time you use this command, you will be guided
    through RSA key setup. When prompted, supply the path to your private key
    to decrypt your passwords.

    After set up, use the `rsa` command to toggle the encryption on and off.
    This can be useful when attempting to share passwords via the 'transfer'
    command to another computer. It's recommended to toggle encryption off
    before transferring, as the encryption keys will not be sent along with the
    password files.

Flags:
    --setup         begin RSA encryption first time set up.
    -v, --verbose   display rsa public and private key during set up.
    -f --force      force RSA setup to overwrite a previously saved key.
        only use this option if encryption is broken and you have no need
        to recover any previously encrypted passwords. They will be lost.
"""


TRANSFER_TEXT = """
Usage: hashword transfer

    This command allows users who have set up SSH connections to their other
    machines to transfer their passwords to that machine securely via SSH.
    Provide the user and the hostname (which can often be found in the
    .ssh/known-hosts file) for the given machine, and hashword will transfer
    the files. To avoid overrwriting any passwords which may already be on that
    machine, the transferred files will have a '.transfer' extension appended.
    It is recommended that encryption is toggled off before transferring, as
    the encryption key on the current machine will not be transferred. See the
    openssh documentation for more details on SSH connections.
"""

# RSA Encryption setup messages below _________________________________________
RSA_SETUP0 = """
RSA Encryption setup: Hashword will create a private and public RSA key for
you. The public key will be stored in the `.hashword/Keys` directory. The
private key will be provided and up to you to store wherever you like. This
private key will need to be provided to access your passwords once encryption
has been set up. Keep this key in a safe place and do not lose it. This may
take a while...
"""

RSA_SETUP1 = """
Encryption setup is complete. Newly generated RSA private and public keys have
been saved in the ../.hashword/Keys/ directory. It is recommended to save the
private key elsewhere for improved security. However, Hashword will always
check in the ../hashword/Keys/ directory for a private key if none is supplied
via the `-k` flag. This is more convenient, but significantly less secure. If
the private key is saved in an alternate location, simply provide the path to
the key using the `-k` flag whenever entering a command.
"""

# Warning & error messages below ----------------------------------------------
WARN_KEYS = """
WARN: Using this program without encryption exposes your saved passwords to
possible theft. If this is your first time using this program, use
`hashword rsa --setupd` to set up encryption.
"""

WARN_MANIFEST_EMPTY = """
WARN: manifest is empty, you may need to restore it. Use the `audit` command to
fix a broken manifest.
"""

WARN_MANIFEST_EXISTS = """
WARN: manifest not found. A new manifest has been created, you may need to
restore it. Use the `audit` command to fix a broken manifest.
"""

WARN_MANIFEST_LOAD = """
WARN: unable to load manifest. A new manifest has been created, you may need to
restore it. Use the `audit` command to fix a broken manifest.
"""


WARN_RSA_OVERWRITE = """
WARN: Rsa encryption has already been set up and a previously saved encryption
key exists. If this key is deleted it may make any encrypted passwords
irretrievable. Use the `-f` flag to force the setup function to overwrite the
old key.
"""

ERROR_MSG = """
Error: {err} Use `hashword --help` for more information.
"""


# Helper functions for printing various important messages below --------------
def print_error(error):
    print(ERROR_MSG.format(err=error))


def print_usage(addendum=False):
    print(USAGE)
    if addendum:
        print("""
    For help with a specific command, run `hashword --help <command>`
    For more in depth help in general, run `hashword --help all`
""")


def display_help(args):
    match len(args):
        case 0:
            print_usage(addendum=True)
        case 1:
            match args[0]:
                case "add":
                    print(ADD_TEXT)
                    print(ADD_FLAGS)
                case "all":
                    print(MAIN_TEXT)
                case "alias":
                    print(ALIAS_TEXT)
                case "audit":
                    print(AUDIT_TEXT)
                case "list":
                    print(LIST_TEXT)
                case "rm":
                    print(RM_TEXT)
                case "data":
                    print(DATA_TEXT)
                case "transfer":
                    print(TRANSFER_TEXT)
                case _:
                    print(NO_ENTRY)
        case _:
            print(NO_ENTRY)
