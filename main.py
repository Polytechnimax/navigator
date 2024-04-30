#! navenv/bin/python


import os
from applescript import tell

from lib.argparser import Parser
from lib.registry import Registry
from lib.misc import bolden, plural, typeof

REGISTRY_FILENAME: str = os.path.expanduser("~/.navconf")            # Name of the file in which the registry is kept on the system


#########################################################
#                        TO ACTION                      #
#########################################################             

def navigate_to(registry: Registry, name: str, in_finder: bool) -> None:
    """
    Executes the `nav to` command: tells the current instance of terminal to move to registered folder and opens a Finder window at this place.

    Args:
        registry (Registry): the registry from which to read the name-path (i.e. key-value) entries
        name (str): name under which the desired path is registered
    """
    if name in registry.invalid:
        print(f"cannot move to {bolden(name)}: invalid entry in the registry\nconsider cleaning your registry")
        return 
    if name in registry.broken:
        print(f"cannot move to {bolden(name)}: corresponding path does not exist\nconsider cleaning your registry") 
        return 
    if name not in registry:
        print(bolden(name) + " is not registered.")
        return
    path = registry[name]
    
    finder_script = f"""
	set screenResolution to bounds of window of desktop
	set rightEdge to item 3 of screenResolution
	set topEdge to item 2 of screenResolution

    open POSIX file \"{path}\"
    
	set the bounds of the front window to {{rightEdge - 900, 0, rightEdge, 600}}

	activate
    """
    terminal_script = f"""    
    do script "cd \\\"{path}\\\"; clear" in front window

	set the bounds of the front window to {0, 0, 900, 600}

    activate
    """
        
    if in_finder: tell.app('Finder', finder_script)
    tell.app('Terminal', terminal_script)

    

#########################################################
#                       LIST ACTION                     #
#########################################################             

def list_registered(registry: Registry, 
                    show_all: bool = False, 
                    show_broken: bool = False, 
                    show_invalid: bool = False, 
                    show_path: bool = False
                    ) -> None:
    """
    Executes the `nav list` command: displays the list of registered folders.
    By default, only names are displayed.
    By default, only valid ones are displayed.

    Args:
        registry (Registry): the registry from which to read the name-path (i.e. key-value) pairs
        show_all (bool, optional): if True, also shows the broken and invalid entries. Overrides show_broken and show_invalid if set to True. Defaults to False.
        show_broken (bool, optional): if True, shows the broken entries and valid ones are not displayed. Defaults to False.
        show_invalid (bool, optional): if True, shows the invalid entries and valid ones are not displayed. Defaults to False.
        show_path (bool, optional): if True, also shows the paths corresponding to names. Defaults to False.
    """
    n_reg, n_brk, n_inv = len(registry), len(registry.broken), len(registry.invalid)
    if show_all or (not show_broken and not show_invalid):
        print(f"{n_reg} {plural('folder', n_reg)} registered:")
        for name, path in registry.items():
            print(f" - {bolden(name)}" + (" (" + path + ")" if show_path else ""))
        if(not show_all and (registry.broken or registry.invalid)): 
            print(f"Warning: you have {n_brk} broken {plural('path', n_brk)} and {n_inv} invalid {plural('entry', n_inv)} in your registry.")
    if show_all or show_broken:
        print(f"{n_brk} broken {plural('path', n_brk)}:")
        for name, path in registry.broken.items():
            print(f" - {bolden(name)}" + (" (" + path + ")" if show_path else ""))
    if show_all or show_invalid:
        print(f"{len(registry.invalid)} invalid {plural('entry', n_inv)}:")
        for name in registry.invalid:
            print(f" - {bolden(name)} (corresponding path of type '{typeof(registry.invalid[name])}')")


#########################################################
#                        ADD ACTION                     #
#########################################################   

def add_to_registry(registry: Registry, 
                    name: str, 
                    path: str
                    ) -> None:   
    """
    Check if the entry is not already in the registry and adds it.

    Args:
        registry (Registry): the registry to add to
        name (str): the key of the path to add
        path (str): the path to the folder to register
    """
    if registry.contains(name, path):
        print("Folder already registered.")
        return
    
    is_valid, is_broken, is_invalid = name in registry, name in registry.broken, name in registry.invalid
    
    if is_valid:
        print(f"{name} is already registered as a valid path ({registry[name]}).")
    if is_broken:
        print(f"{name} is already registered as a broken path ({registry.broken[name]}).")
    if is_invalid:
        print(f"{name} is already registered as an invalid entry.")
    
    while is_valid or is_broken or is_invalid:
        ans = input(f"Do you wish to replace it? (y/N) ")
        if ans.lower() in { 'no', 'n', '' }:
            return
        if ans.lower() in { 'yes', 'y'}:
            break
        print(bolden('Unrecognised answer.'))
    
    if is_broken: del registry.broken[name]
    if is_invalid: del registry.invalid[name]
    registry[name] = path 
    registry.write_to(REGISTRY_FILENAME)
        
        
#########################################################
#                        DEL ACTION                     #
#########################################################   
        
def del_from_registry(registry: Registry, 
                      name: str
                      ) -> None:
    """
    Executes the `nav del` command: removes the specified name from the registry.

    Args:
        registry (Registry): the registry to remove from
        name (str): the name of the entry to be removed
    """
    try:
        registry.delete(name)
        registry.write_to(REGISTRY_FILENAME)
    except KeyError:
        print(f"{name} does not correspond to any (valid, broken or invalid) registered folder.")


#########################################################
#                       CLEAN ACTION                    #
#########################################################   

def clean(registry: Registry, 
          clean_broken: bool = True, 
          clean_invalid : bool = True
          ) -> None:
    """
    Executes the `nav clean` command: removes broken and/or invalid entries from the registry.

    Args:
        registry (Registry): the registry to clean
        clean_broken (bool, optional): whether broken entries should be removed. Defaults to True.
        clean_invalid (bool, optional): whether invalid entries should be removed. Defaults to True.
    """
    if clean_broken: registry.clean_broken()
    if clean_invalid: registry.clean_invalid()
    registry.write_to(filename=REGISTRY_FILENAME)


#########################################################
#                       MAIN LOGIC                      #
######################################################### 

def act(registry: Registry, 
        args: dict[str, str | bool]
        ) -> None:
    """
    Executes the desired `nav` command.

    Args:
        registry (Registry): the registry with which to perform the action
        args (dict[str, str  |  bool]): the arguments given in the CLI
    """
    match args['action']:
        case "to":
            navigate_to(registry=registry, 
                        name=args['name'], 
                        in_finder=args['in_finder'])
        case "list":
            list_registered(registry=registry, 
                            show_all=args['show_all'], 
                            show_broken=args['show_broken'], 
                            show_invalid=args['show_invalid'], 
                            show_path=args['show_path'])
        case "add":
            add_to_registry(registry=registry, 
                            name=args['name'], 
                            path=args['path'])
        case "del":
            del_from_registry(registry=registry, 
                              name=args['name'])
        case "clean":
            clean_broken: bool = args['clean_broken'] or not args['clean_invalid']
            clean_invalid: bool = args['clean_invalid'] or not args['clean_broken']
            clean(registry=registry, clean_broken=clean_broken, clean_invalid=clean_invalid)
        case _:
            raise NotImplementedError
                       
def main() -> None:
    registry = Registry(REGISTRY_FILENAME)
    parser = Parser(registry=registry)
    act(registry=registry, args=parser.args)    

if __name__ == "__main__":
    main()