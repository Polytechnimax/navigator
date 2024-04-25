import os

def bolden(text: str) -> str:    
    """
    Returns a bold version of the text.

    Args:
        text (str): the text to return bold

    Returns:
        str: the bold version of text
    """

    return "\033[1m" + text + "\033[0m"

def abspath(path: str) -> str:
    """
    Returns the absolute version of the path given in argument.

    Args:
        path (str): the path to return in its absolute version

    Returns:
        str: the absolute version of the path
    """
    return os.path.abspath(os.path.expanduser(path))

def dir_exists(path: str) -> bool:
    """
    Checks whether the specified path is a valid path to a directory.

    Args:
        path (str): the path to check

    Returns:
        bool: True if the path corresponds to a directory, False otherwise 
    """
    return os.path.isdir(abspath(path))