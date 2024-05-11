# import rsa
import sys
from hashword import HashWord as hword
from hashword import PwData

if __name__ == "__main__":

    h = hword()
    # TODO: only run populate if needed
    h.populate()
    try:
        match sys.argv[1]:
            case 'add':
                h.create()
            case 'list':
                h.list_self()
            case 'del':
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
                    print("Usage:\n\thashword add\n\thashword list" +
                          "\n\thashword <name of password>" +
                          "\n\thashword del <name of password>" +
                          "\n\thashword alias <name of password> <alias>")
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
                    print("Usage:\n\thashword add\n\thashword list" +
                          "\n\thashword <name of password>" +
                          "\n\thashword del <name of password>" +
                          "\n\thashword alias <name of password> <alias>")
            case '--help':
                print("'--help':\n\thashword add\n\thashword list" +
                      "\n\thashword <name of password>" +
                      "\n\thashword del <name of password>" +
                      "\n\thashword alias <name of password> <alias>")

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
