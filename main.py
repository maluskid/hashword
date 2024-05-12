from hashword import HashWord as hword
import helptext as help
import rsa
import sys


def print_usage(addendum=False):
    print(help.USAGE)
    if addendum:
        print("\tFor help with a specific command, " +
              "run `hashword --help <command>`\n\t" +
              "For more in depth help in general, run " +
              "`hashword --help all`\n")


def display_help():
    match len(sys.argv):
        case 2:
            print("hashword <command>")
            print_usage(addendum=True)
        case 3:
            match sys.argv[2]:
                case 'add':
                    print(help.ADD_TEXT)
                case 'all':
                    print(help.MAIN_TEXT)
                case 'alias':
                    print(help.ALIAS_TEXT)
                case 'list':
                    print(help.LIST_TEXT)
                case 'rm':
                    print(help.RM_TEXT)
                case 'rsa':
                    print(help.RSA_TEXT)
                case _:
                    print(help.NO_ENTRY)
        case _:
            print(help.NO_ENTRY)


def execute_add():
    name = input("Enter a name for new passcode:\n")
    size = int(input("What is the max character" +
                     "count for this password?\n"))
    algo = input("Choose a hashing algorithm:\n\t1) sha256" +
                 "\n\t2) md5\n\t3) sha-3\n\t4) blake2b\n")
    seed = input("Choose a seed to create your password" +
                 "with or press Enter:\n").strip()
    h.create(name, size, algo, seed)


if __name__ == "__main__":

    h = hword()
    try:
        match sys.argv[1]:
            case 'add':
                try:
                    execute_add()
                except Exception as e:
                    print("Error {err} adding new password".format(err=e))
            case 'alias':
                try:
                    if sys.argv[2] in h:
                        h[sys.argv[2]].add_alias(sys.argv[3])
                    else:
                        for key in h:
                            if sys.argv[2] in h[key].alias_list:
                                h[key].add_alias(sys.argv[3])
                                break
                except Exception as e:
                    print("Error {err} encountered deleting".format(err=e))
                    print_usage()
            case 'list':
                h.list_self()
            case 'rm':
                try:
                    if sys.argv[2] in h:
                        h.delete(sys.argv[2])
                    else:
                        for key in h:
                            if sys.argv[2] in h[key].alias_list:
                                h.delete(h[key])
                                break
                except Exception as e:
                    print("Error {err} encountered deleting".format(err=e))
                    print_usage()
            case 'rsa':
                try:
                    pass
                except Exception as e:
                    print("Error {err} encountered during rsa generation"
                          .format(err=e))
            case '--help':
                display_help()
            case _:
                inlist = False
                if sys.argv[1] in h:
                    print(h[sys.argv[1]].getpw())
                    inlist = True
                else:
                    for key in h:
                        if sys.argv[1] in h[key].alias_list:
                            print(h[key].getpw())
                            inlist = True
                            break
                if not inlist:
                    print("'{name}' not found in list.".format(
                        name=sys.argv[1]))

    except Exception:
        print("Invalid argument. Input `hashword --help` to view usage " +
              "information.")

    h.save()
