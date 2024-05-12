import random
import base64
from hashword import seed_generator, HashWord as hword
import helptext as help
import rsa
import sys


def print_usage(addendum=False):
    print(help.USAGE)
    if addendum:
        print(
            "\tFor help with a specific command, "
            + "run `hashword --help <command>`\n\t"
            + "For more in depth help in general, run "
            + "`hashword --help all`\n"
        )


def display_help():
    match len(sys.argv):
        case 2:
            print("hashword <command>")
            print_usage(addendum=True)
        case 3:
            match sys.argv[2]:
                case "add":
                    print(help.ADD_TEXT)
                case "all":
                    print(help.MAIN_TEXT)
                case "alias":
                    print(help.ALIAS_TEXT)
                case "list":
                    print(help.LIST_TEXT)
                case "rm":
                    print(help.RM_TEXT)
                case "rsa":
                    print(help.RSA_TEXT)
                case _:
                    print(help.NO_ENTRY)
        case _:
            print(help.NO_ENTRY)


def execute_add(options):
    match options:
        case {"name": opt_name} if not opt_name:
            raise (ValueError("No name provided for new password.\n"))
        case {"name": name,
              "size": size,
              "algo": algo,
              "seed": seed}:
            h.create(name, size, algo, seed)
        case _:
            raise (Exception("An unforseen circumstance has arisen"))


def parse_args():
    argslist = []
    options = {
        "name": None,
        "size": None,
        "algo": None,
        "seed": None,
    }
    try:
        match sys.argv:
            case [_, "add", *opts]:
                argslist.append("add")
                # *_ used instead of *rest to keep linter from arguing
                # should match situations where the pattern exists even
                # if the list is longer than two elements.
                match opts:
                    case [("-n" | "--name"), value, *_]:
                        if not options["name"]:
                            options["name"] = value
                        else:
                            raise (ValueError("Duplicate opts found."))
                    case [("-S" | "--seed"), value, *_]:
                        if not options["seed"]:
                            options["seed"] = value
                        else:
                            raise (ValueError("Duplicate opts found."))
                    case [("-s" | "--size"), value, *_]:
                        if not options["size"]:
                            options["size"] = value
                        else:
                            raise (ValueError("Duplicate opts found."))
                    case [("-a" | "--algorithm"),
                          ("md5" | "sha256" | "sha-3" | "blake2b") as value,
                          *_]:
                        if not options["algo"]:
                            options["algo"] = value
                        else:
                            raise (ValueError("Duplicate opts found."))
                    case [("-a" | "--algorithm"), _]:
                        raise (ValueError("Invalid algorithm supplied."))
                    case []:
                        pass
            case [_, *args]:
                for arg in args:
                    argslist.append(arg)
            case _:
                raise (ValueError("No arguments detected."))
    except Exception as e:
        if e == ValueError:
            print("Error: {err} Arguments for `hashword add` not recognised. \
            Use `hashword --help add` to view syntax information."
                  .format(err=e))
        else:
            print("Error: {err} Use `hashword --help` to view usage\
             information.".format(err=e))

    return [argslist, options]


if __name__ == "__main__":
    h = hword()
    [argslist, optslist] = parse_args()

    match argslist[0]:
        case "add":
            try:
                execute_add(argslist)
            except Exception as e:
                print("Error {err} adding new password".format(err=e))
        case "alias":
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
        case "list":
            h.list_self()
        case "rm":
            try:
                h.delete(argslist[1])
            except Exception as e:
                print("Error {err} encountered deleting".format(err=e))
                print_usage()
        case "rsa":
            try:
                # TODO
                pass
            except Exception as e:
                print("Error {err} encountered during rsa generation"
                      .format(err=e))
        case "--help":
            display_help()
        case _:
            try:
                h.get(argslist[0])
            except Exception:
                match Exception:
                    case KeyError() as e:
                        print("Error {err} encountered looking for {item} in \
                        manifest.".format(err=e, item=argslist[0]))
                    case _ as e:
                        print("Error {err} encountered deleting {item}"
                              .format(err=e, item=argslist[0]))

                print("'{name}' not found in list.".format(name=sys.argv[1]))

h.save()
