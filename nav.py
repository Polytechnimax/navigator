# shebang line

# TODO -- Unify the access to the registry and handle errors
# TODO -- Implement the doctor keyword
# TODO -- Improve the helper
# TODO -- Fix the VSCode import
# TODO -- Improve the switch between test and production
# TODO -- Create a specific python environment (done but needs a better incorporation with the switch between test & production)

import os
import sys
from applescript import tell

REGISTRY = os.path.expanduser("~/.navconf")
from lib.argparser import Parser
from lib.register import Register
from lib.misc import bolden, path_exists



#########################################################
#                        TO ACTION                      #
#########################################################             
def navigate_to(name):
    register = Register(REGISTRY)
    if name not in register:
        print(bolden(name) + " is not registered.")
        return
    path = register[name]
    if not path_exists(path):
        print("Registered path (" + path + ") does not exist.")
        # TODO -- Offer to delete?
        return
    
    # as_path = applescript_path(path)
    tell.app('Terminal', f'do script "cd \\\"{path}\\\"; clear" in front window')
    tell.app('Terminal', 'activate')    
    tell.app('Finder', f'open POSIX file \"{path}\"')
    tell.app('Finder', 'activate')
    # TODO -- Move and resize windows

    

#########################################################
#                       LIST ACTION                     #
#########################################################             
def list_registered(show_path=False):
    register = Register(REGISTRY)
    print(f"{len(register)} folders registered:")
    for name, path in register.items():
        print(" > " + bolden(name) + (" (" + path + ")" if show_path else ""))


#########################################################
#                        ADD ACTION                     #
#########################################################   

def add_to_register(name, path):   
    register = Register(REGISTRY)
    if register.contains(name, path):
        print("Folder already registered.")
        return
    if register.contains(name):
        while True:
            ans = input(f"Another folder is already registered under this name.({register[name]})\nDo you wish to replace it? (y/N) ")
            if ans.lower() in { 'no', 'n', '' }:
                return
            if ans.lower() in { 'yes', 'y'}:
                break
            print(bolden('Unrecognised answer.'))
    register[name] = path 
    register.write_to(REGISTRY)
        
        
#########################################################
#                        DEL ACTION                     #
#########################################################   
        
def del_from_register(name):
    register = Register(REGISTRY)
    if register.contains(name):
        path = register[name]
        del register[name]
        register.write_to(REGISTRY)
    else:
        print("No folder with this name registered.")



#########################################################
#                       MAIN LOGIC                      #
######################################################### 

def act(args):
    match args.action:
        case "to":
            navigate_to(name=args.name)
        case "list":
            list_registered(show_path = args.show_path)
        case "add":
            add_to_register(name=args.name, path=args.path)
        case "del":
            del_from_register(name=args.name)
            pass

def main():
    parser = Parser()
    act(parser.args)    

if __name__ == "__main__":
    main()