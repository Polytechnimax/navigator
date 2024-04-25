#! /Users/larcherm/Documents/Programmation/Automation/navigator/navenv/bin/python

# TODO -- Improve the registry's handling of the broken and invalid entries
# TODO -- Implement the doctor keyword
# TODO -- Improve the helper
# TODO -- Improve the description in the main file


import os
from applescript import tell
import logging


REGISTRY = os.path.expanduser("~/.navconf")
from lib.argparser import Parser
from lib.registry import Registry
from lib.misc import bolden, dir_exists



#########################################################
#                        TO ACTION                      #
#########################################################             
def navigate_to(registry, name):
    if name not in registry:
        print(bolden(name) + " is not registered.")
        return
    path = registry[name]
    if not dir_exists(path):
        print("registered path (" + path + ") does not exist.")
        # TODO -- Offer to delete?
        return
    
    tell.app('Terminal', f'do script "cd \\\"{path}\\\"; clear" in front window')
    tell.app('Terminal', 'activate')    
    tell.app('Finder', f'open POSIX file \"{path}\"')
    tell.app('Finder', 'activate')
    # TODO -- Move and resize windows

    

#########################################################
#                       LIST ACTION                     #
#########################################################             
def list_registered(registry: Registry, show_all: bool = False, show_broken: bool = False, show_invalid: bool = False, show_path: bool = False):
    n_reg, n_brk, n_inv = len(registry), len(registry.broken), len(registry.invalid)
    if show_all or (not show_broken and not show_invalid):
        print(f"{n_reg} folder{'' if n_reg<=1 else 's'} registered:")
        for name, path in registry.items():
            print(f" - {bolden(name)}" + (" (" + path + ")" if show_path else ""))
        if(not show_all and (registry.broken or registry.invalid)): 
            print(f"Warning: you have {n_brk} broken path{'' if n_brk<=1 else 's'} and {n_inv} invalid entr{'y' if n_inv<=1 else 'ies'} in your registry.")
    if show_all or show_broken:
        print(f"{n_brk} broken path{'' if n_brk<=1 else 's'}:")
        for name, path in registry.broken.items():
            print(f" - {bolden(name)}" + (" (" + path + ")" if show_path else ""))
    if show_all or show_invalid:
        print(f"{len(registry.invalid)} invalid entr{'y' if n_inv<=1 else 'ies'}:")
        for name in registry.invalid:
            print(f" - {bolden(name)}")


#########################################################
#                        ADD ACTION                     #
#########################################################   

def add_to_registry(registry, name, path):   
    if registry.contains(name, path):
        print("Folder already registered.")
        return
    is_valid, is_broken, is_invalid = name in registry, name in registry.broken, name in registry.invalid
    if is_valid or is_broken or is_invalid:
        print(f"{name} is already registered ({f"valid path {registry[name]})" if is_valid else f"broken path {registry.broken[name]})" if is_broken else "invalid)"}.")
        while True:
            ans = input(f"Do you wish to replace it? (y/N) ")
            if ans.lower() in { 'no', 'n', '' }:
                return
            if ans.lower() in { 'yes', 'y'}:
                break
            print(bolden('Unrecognised answer.'))
    if name in registry.broken: del registry.broken[name]
    if name in registry.invalid: del registry.invalid[name]
    registry[name] = path 
    registry.write_to(REGISTRY)
        
        
#########################################################
#                        DEL ACTION                     #
#########################################################   
        
def del_from_registry(registry, name):
    if name in registry:
        path = registry[name]
        del registry[name]
        registry.write_to(REGISTRY)
    elif name in registry.broken:
        del registry.broken[name]
        registry.write_to(REGISTRY)
    elif name in registry.invalid:
        del registry.invalid[name]
        registry.write_to(REGISTRY)
    else:
        print(f"{name} does not correspond to a (valid, broken or invalid) registered folder.")



#########################################################
#                       MAIN LOGIC                      #
######################################################### 

def act(registry, args):
    match args.action:
        case "to":
            navigate_to(registry=registry, name=args.name)
        case "list":
            list_registered(registry=registry, show_all=args.show_all, show_broken=args.show_broken, show_invalid=args.show_invalid, show_path=args.show_path)
        case "add":
            add_to_registry(registry=registry, name=args.name, path=args.path)
        case "del":
            del_from_registry(registry=registry, name=args.name)
            pass

def main():
    registry = Registry(REGISTRY)
    parser = Parser(registry=registry)
    act(registry=registry, args=parser.args)    

if __name__ == "__main__":
    main()