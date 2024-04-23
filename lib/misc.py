import os

def bolden(text: str):    
    return "\033[1m" + text + "\033[0m"

def abspath(path: str):
    return os.path.abspath(os.path.expanduser(path))

def path_exists(path: str):
    return os.path.isdir(path)