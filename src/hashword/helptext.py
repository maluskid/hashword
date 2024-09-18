# Most of the text output for the various functions in hashword is stored here
# to reduce clutter and make consistent formatting easier.

# Important help text below ---------------------------------------------------
USAGE = "Usage:\n\thashword <foo>\t\t\tshow hash for <foo>" \
    "\n\thashword add\t\t\tadd new password" \
    "\n\thashword alias <foo> <alias>\talias <foo> as <alias>" \
    "\n\thashword audit\t\t\taudits saved aliases and passwords" \
    "\n\thashword data\t\t\tshow path to `/.hashword/data`" \
    "\n\thashword list\t\t\tlist saved passwords" \
    "\n\thashword rm <foo>\t\tremove <foo>" \
    "\n\thashword rsa\t\t\tmanage RSA keys\n\n"

NO_ENTRY = "\t\tThere isn't a help entry written for that yet . If you have" \
    "\n\tsuggestions for\nimproving Hashword or find any issues, report them" \
    "\n\tat https://github.com/maluskid/hashword/issues.\n"

MAIN_TEXT = "\tUsage: hashword <foo>\n" \
    "\n\tPrint the hash of the saved value corresponding to <foo> or any" \
    "\n\tpassword <foo> is an alias of to STDOUT. Use `hashword list` to" \
    "\n\tview stored passwords and aliases. All data is stored in the home" \
    "\n\tdirectory. The path to this directory can be found with `hashword" \
    "\n\tdata` Use `hashword rm <foo>` to remove all data pertaining to" \
    "\n\t <foo> from the data directory. This *CANNOT* be undone, so use" \
    "\n\tcaution when executing this command." \
    "\n\n\tCopying from the terminal to your clipboard is OS dependant," \
    "\n\tplease consult the relevant documentation accordingly. Some common" \
    "\n\tdefault commands are listed below:" \
    "\n\n\tWindows Powershell - <ctrl-c>" \
    "\n\tGnome Terminal  - <ctrl-shift-c>" \
    "\n\tMac Terminal - <cmd-c>\n"

# Help entries in alphabetical order below ------------------------------------
ADD_TEXT = "\tUsage: hashword add\n" \
    "\n\tThis command will begin a step by step process in the terminal to" \
    "\n\tadd a new password to the keyring. Multiple hashing algorithms are" \
    "\n\tavailable to select from:\n\tsha256, blake2b, md5, sha-3" \
    "\n\tIf none is supplied, sha256 is the default. If desired, the user" \
    "\n\tcan supply a certain input to be the seed for the resultant hash." \
    "\n\tThis allows the user to reproduce the same hashed password value"\
    "\n\tacross multiple computers all running hashword. If no seed is" \
    "\n\tprovided, a randomized seed is produced. And kept hidden. This" \
    "\n\toption provides maximum security, but makes it impossible to" \
    "\n\trecreate the password if lost or away from the computer used to" \
    "\n\tgenerate it." \
    "\n\n\tSeeds are stored with the rest of password data in the encrypted" \
    "\n\tfiles located in `../.hashword/data`. The full path to this" \
    "\n\tdirectory can be viewed with the `data` command."

ALIAS_TEXT = "\tUsage: hashword alias <foo> <alias>\n" \
    "\n\tThis command will link the password <foo> to an alias <alias>." \
    "\n\tAny subsequent calls to hashword will treat any command using" \
    "\n\t<alias> the same as though it were entered using <foo>. You can" \
    "\n\tview all aliases with the `list` command.\n"

AUDIT_TEXT = "\tUsage: hashword audit\n" \
    "\n\tThis command will perform an audit of the saved `manifest.json` and" \
    "\n\tall saved passwords. Use this command if an old password isn't" \
    "\n\trecognized after a fresh installation. Aliases previously assigned" \
    "\n\tto an old password entry will be lost and must be reassigned. If a" \
    "\n\tpassword file has been removed without the use of the `rm` command," \
    "\n\tthis command will fix the broken manifest.\n"

DATA_TEXT = "\tUsage: hashword data\n" \
    "\n\tThis command will display path to the data directory where all" \
    "\n\tpassword data is stored. If RSA encryption hasn't been set up," \
    "\n\tthese files are incredibly easy to gain information from. For" \
    "\n\tyour data safety, using RSA encryption is highly recommended.\n"

LIST_TEXT = "\tUsage: hashword list\n" \
    "\n\tThis command displays all saved passwords as well as any aliases" \
    "\n\tassigned to them.\n"

RM_TEXT = "\tUsage: hashword rm <foo>\n" \
    "\n\tThis command removes all files stored in the .hashword/data/" \
    "\n\tdirectory pertaining to <foo>. This *CANNOT* be undone, so use care" \
    "\n\twhen executing this command. Making a backup is recommended, all" \
    "\n\tare named by the password they refer to. Hashword encrypts all" \
    "\n\tpassword files with your RSA public key before saving them.\n"

RSA_TEXT = "\tUsage: hashword rsa\n" \
    "\n\tThis software uses RSA keys to verify your identity and protect" \
    "\n\tyour passwords. The rsa command will begin a step by step process" \
    "\n\tin the terminal to complete first time setup or manage RSA keys." \
    "\n\tPasswords are encrypted using your public key. In order to decrypt" \
    "\n\tthem, you must supply your private key. The first time you use this" \
    "\n\tprogram, you will be guided through RSA key setup. When prompted," \
    "\n\tsupply the path to your private key to decrypt your passwords.\n\n" \
    "\n\tFlags:" \
    "\n\t\t-v, --verbose\t\tdisplay rsa public and private key in STDOUT." \
    "\n\t\t-f --force\t\tforce RSA setup to overwrite a previously saved key."

# RSA Encryption setup messages below _________________________________________
RSA_SETUP0 = "\tRSA Encryption setup:" \
    "\n\tHashword will create a private and public RSA key for you. The" \
    "\n\tpublic key will be stored in the `.hashword/Keys` directory. The" \
    "\n\tprivate key will be provided and up to you to store wherever you" \
    "\n\tlike. This private key will need to be provided to access your" \
    "\n\tpasswords once encryption has been set up. Keep this key in a safe" \
    "\n\tplace and do not lose it.\n"

RSA_SETUP1 = "\tRSA Encryption setup:" \
    "\n\tEncryption setup is complete. Your private and public keys have" \
    "\n\tbeen saved in the current working directory.\n"

# Warning & error messages below ----------------------------------------------
WARN_KEYS = "\n\tWARN: Using this program without encryption exposes your" \
    "\n\tsaved passwords to possible theft. If this is your first time using" \
    "\n\tthis program, use `hashword rsa` to set up encryption.\n"

WARN_MANIFEST = "\n\tWARN: manifest.json is empty, you may need to restore" \
    "\n\tit. Use the `audit` command to fix a broken manifest.\n"

WARN_RSA_OVERWRITE = "\n\tWARN: Rsa encryption has already been set up and" \
    "\n\ta previously saved encryption key exists. If this key is deleted" \
    "\n\tit may make any encrypted passwords irretrievable. Use the `-f`" \
    "\n\tflag to force the setup function to overwrite the old key.\n"

ERROR_MSG = "Error: {err} Use `hashword --help` for more information.\n"


# Helper functions for printing various important messages below --------------
def print_error(error):
    print(ERROR_MSG.format(err=error))


def print_usage(addendum=False):
    print(USAGE)
    if addendum:
        print("\tFor help with a specific command, "
              + "run `hashword --help <command>`\n\t"
              + "For more in depth help in general, run "
              + "`hashword --help all`\n")


def display_help(args):
    match len(args):
        case 0:
            print("hashword <command>")
            print_usage(addendum=True)
        case 1:
            match args[0]:
                case "add":
                    print(ADD_TEXT)
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
                case "rsa":
                    print(RSA_TEXT)
                case "data":
                    print(DATA_TEXT)
                case _:
                    print(NO_ENTRY)
        case _:
            print(NO_ENTRY)
