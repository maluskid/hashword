# Most of the longer text outputs for the help functionality is stored here
# to reduce clutter and make consistent formatting easier.

USAGE = "Usage:\n\thashword <foo>\t\t\tshow hash for <foo>" \
    "\n\thashword add\t\t\tadd new password" \
    "\n\thashword alias <foo> <alias>\talias <foo> as <alias>" \
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
    "\n\tprogram, supply your public key. When prompted, supply the path to" \
    "\n\tyour private key. You can store this path with Haswhord, but be" \
    "\n\twary that this constitues a security risk.\n"

ERROR_MSG = "Error: {err} Use `hashword --help` for more information."


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
        case 1:
            print("hashword <command>")
            print_usage(addendum=True)
        case 2:
            match args[2]:
                case "add":
                    print(ADD_TEXT)
                case "all":
                    print(MAIN_TEXT)
                case "alias":
                    print(ALIAS_TEXT)
                case "list":
                    print(LIST_TEXT)
                case "rm":
                    print(RM_TEXT)
                case "rsa":
                    print(RSA_TEXT)
                case _:
                    print(NO_ENTRY)
        case _:
            print(NO_ENTRY)
