#! /bin/python3
import sys
from hashword import HashWord as hword
from hashword import print_error as perror
from hashword import print_usage as pusage
from hashword import display_help as phelp


def execute_add(options):

    match options:
        case {"name": opt_name} if not opt_name:
            raise (ValueError("No name provided for new password.\n"))
        case {"algo": algo,
              "name": name,
              "seed": seed,
              "size": size,
              "keypath": rsapath}:
            return (algo, name, seed, size, rsapath)
        case _:
            raise (Exception("An unforseen circumstance has arisen"))


def parse_args():
    argslist = []
    options = {
        "algo": None,
        "name": None,
        "seed": None,
        "size": None,
        "keypath": None,
        "force": None,
        "verbose": None
    }
    try:
        match sys.argv:
            case [_, "add", *opts]:
                argslist.append("add")
                match len(opts):
                    case val if val % 2 == 0:
                        raise (ValueError("Incorrect argument format."))
                    case val if val % 2 == 1:
                        options["name"] = opts.pop()
                        while opts:
                            match [opts.pop(0), opts.pop(0)]:
                                case [('-a' | '--algorithm'), value]:
                                    options["algo"] = value
                                case [('-S' | '--seed'), value]:
                                    options["seed"] = value
                                case [('-s' | '--size'), value]:
                                    options["size"] = int(value)
                                case [('-k' | '--key'), value]:
                                    options["keypath"] = value
                                case [first, second]:
                                    errormsg = "Option {f} {s} not recognized."
                                    errormsg.format(f=first, s=second)
                                    raise (ValueError(errormsg))
            case [_, *args] if len(args) < 1:
                raise (RuntimeError("No arguments detected."))
            case [_, *args] if len(args) >= 1:
                while args:
                    match args.pop(0):
                        case ('-f' | '--force'):
                            options["force"] = True
                        case ('-v' | '--verbose'):
                            options["verbose"] = True
                        case ('-k' | '--key'):
                            if args:
                                options["keypath"] = args.pop(0)
                            else:
                                errormsg = "Invalid use of `-k` flag."
                                raise (ValueError(errormsg))
                        case val:
                            argslist.append(val)
            case _:
                raise (Exception("Something unexpected ocurred."))
    except ValueError as e:
        perror(e)
    except RuntimeError as e:
        perror(e)
        pusage(addendum=True)
        sys.exit(0)
    except Exception as e:
        perror(e)

    return [argslist, options]


if __name__ == "__main__":
    h = hword()
    [argslist, optslist] = parse_args()
    match argslist[0]:
        case "add":
            [algo, name, seed, size, rsapath] = execute_add(optslist)
            h.create(algo, name, seed, size, rsapath)
            name = optslist["name"]
            print("Hashword {n} successfully added."
                  .format(n=name))
        case "alias":
            h.alias(argslist[1], argslist[2])
        case "list":
            h.list_self()
        case "rm":
            h.delete(argslist[1])
        case "rsa":
            v = False
            if optslist["verbose"]:
                v = True
            # try:
            h.rsa(optslist["force"], optslist["verbose"])
            # except Exception as e:
            #     perror(e)
        case "data":
            print("Password data saved at {location}".format(
                location=h.showpath()))
        case "--help":
            argslist.pop(0)
            phelp(argslist)
        case 'audit':
            print("Beginning audit...")
            h.audit(optslist["keypath"])
            print("Audit complete!")
            h.list_self()
        case 'undo':
            h.rsa_undo()
            h.audit()
        case arg:
            print(h.get(arg, optslist["keypath"]))
