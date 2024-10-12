# Most of the text output for the various functions in hashword is stored here
# to reduce clutter and make consistent formatting easier.

# Important help text below ---------------------------------------------------
USAGE = "Usage:\n\thashword <foo>\t\t\tshow hash for <foo>" \
    "\n\thashword add <flags> <foo>\tadd new password named <foo>" \
    "\n\thashword alias <foo> <alias>\talias <foo> as <alias>" \
    "\n\thashword audit\t\t\taudits saved aliases and passwords" \
    "\n\thashword data\t\t\tshow path to `/.hashword/data`" \
    "\n\thashword list\t\t\tlist saved passwords" \
    "\n\thashword rm <foo>\t\tremove <foo>"

NO_ENTRY = "\t\tThere isn't a help entry written for that yet . If you have" \
    "\n\tsuggestions for\nimproving Hashword or find any issues, report them" \
    "\n\tat https://github.com/maluskid/hashword/issues.\n"

MAIN_TEXT = "Usage: hashword <foo>\n" \
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
ADD_TEXT = "Usage: hashword add\n" \
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
    "\n\tdirectory can be viewed with the `data` command." \
    "\n\nFlags: -a, -S, -s\n" \
    "\n\t(-a || --algorithm) <foo> Determines which algorithm to use." \
    "\n\tIf no value is supplied, the default sha256 hash will be used." \
    "\n\tValid inputs: blake2b, md5, sha256, sha-3\n" \
    "\n\t(-S || --seed) <foo> Determines a seed phrase for the hashed" \
    "\n\tpassword. If no value is supplied, a randomized seed will be used." \
    "\n\tIt will be impossible to recreate this hash without specifying a" \
    "\n\tseed.\n" \
    "\n\t(-s || --size) <int> Sets the length of the hex string output of" \
    "\n\tthe hash. Defaults to maximum size for pertaining algorithm, if a" \
    "\n\tnumber larger than the algorithm supports is entered, the default is" \
    "\n\tused."


ALIAS_TEXT = "Usage: hashword alias <foo> <alias>\n" \
    "\n\tThis command will link the password <foo> to an alias <alias>." \
    "\n\tAny subsequent calls to hashword will treat any command using" \
    "\n\t<alias> the same as though it were entered using <foo>. You can" \
    "\n\tview all aliases with the `list` command.\n"

AUDIT_TEXT = "Usage: hashword audit\n" \
    "\n\tThis command will perform an audit of the saved `manifest.json` and" \
    "\n\tall saved passwords. Use this command if an old password isn't" \
    "\n\trecognized after a fresh installation. Aliases previously assigned" \
    "\n\tto an old password entry will be lost and must be reassigned. If a" \
    "\n\tpassword file has been removed without the use of the `rm` command," \
    "\n\tthis command will fix the broken manifest.\n"

DATA_TEXT = "Usage: hashword data\n" \
    "\n\tThis command will display path to the data directory where all" \
    "\n\tpassword data is stored. If RSA encryption hasn't been set up," \
    "\n\tthese files are incredibly easy to gain information from. For" \
    "\n\tyour data safety, using RSA encryption is highly recommended.\n"

LIST_TEXT = "Usage: hashword list\n" \
    "\n\tThis command displays all saved passwords as well as any aliases" \
    "\n\tassigned to them.\n"

RM_TEXT = "Usage: hashword rm <foo>\n" \
    "\n\tThis command removes all files stored in the .hashword/data/" \
    "\n\tdirectory pertaining to <foo>. This *CANNOT* be undone, so use care" \
    "\n\twhen executing this command. Making a backup is recommended, all" \
    "\n\tare named by the password they refer to. Hashword encrypts all" \
    "\n\tpassword files with your RSA public key before saving them.\n"

# Warning & error messages below ----------------------------------------------
WARN_MANIFEST = "\nWARN: manifest.json is empty, you may need to restore it." \
    "\n\tUse the `audit` command to fix a broken manifest.\n"

ERROR_MSG = "Error: {err} Use `hashword --help` for more information.\n"


# Helper functions for printing various important messages below --------------
def print_error(error):
    print(ERROR_MSG.format(err=error))


def print_usage(addendum=False):
    print(USAGE)
    if addendum:
        print("\n\tFor help with a specific command, "
              + "run `hashword --help <command>`\n\n\t"
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
                case "data":
                    print(DATA_TEXT)
                case _:
                    print(NO_ENTRY)
        case _:
            print(NO_ENTRY)
