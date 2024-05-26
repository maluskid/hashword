from hashword import HashWord as hword
import helptext as help
# import rsa
import sys


def execute_add(options):

    match options:
        case {"name": opt_name} if not opt_name:
            raise (ValueError("No name provided for new password.\n"))
        case {"algo": algo,
              "name": name,
              "seed": seed,
              "size": size}:
            h.create(algo, name, seed, size)
        case _:
            raise (Exception("An unforseen circumstance has arisen"))


def parse_args():
    argslist = []
    options = {
        "algo": None,
        "name": None,
        "seed": None,
        "size": None,
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
                                case [first, second]:
                                    errormsg = "Option {f} {s} not recognized."
                                    errormsg.format(f=first, s=second)
                                    raise (ValueError(errormsg))
            case [_, *args] if len(args) < 1:
                raise (RuntimeError("No arguments detected."))
            case [_, *args] if len(args) >= 1:
                for arg in args:
                    argslist.append(arg)
            case _:
                raise (Exception("Something unexpected ocurred."))
    except ValueError as e:
        help.print_error(e)
    except RuntimeError as e:
        help.print_error(e)
        help.print_usage(addendum=True)
        sys.exit(0)
    except Exception as e:
        help.print_error(e)

    return [argslist, options]


if __name__ == "__main__":
    h = hword()
    [argslist, optslist] = parse_args()
    match argslist[0]:
        case "add":
            try:
                execute_add(optslist)
            except Exception as e:
                help.print_error(e)
            name = optslist["name"]
            print("Hashword {n} successfully added."
                  .format(n=name))
        case "alias":
            try:
                h.alias(argslist[1], argslist[2])
            except Exception as e:
                help.print_error(e)
                help.print_usage()
        case "list":
            h.list_self()
        case "rm":
            try:
                h.delete(argslist[1])
            except Exception as e:
                help.print_error(e)
                help.print_usage()
        case "rsa":
            try:
                # TODO
                pass
            except Exception as e:
                help.print_error(e)
        case "--help":
            help.display_help(argslist)
        case 'audit':
            print("Beginning audit...")
            h.audit()
            print("Audit complete!")
            h.list_self()
        case arg:
            try:
                target = h.get(arg)
                print(target.getpw())
            except KeyError as e:
                help.print_error(e)
            except Exception as e:
                help.print_error(e)
