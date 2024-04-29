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


def plural(word: str, count: int = 2) -> str:
    """
    Returns the plural of a word.
    Is designed to be extremely fast and was only thought for navigator, so it cannot be ported.

    Args:
        word (str): the word to return plural
        count (int, optional): if the value is <=1, the word is kept singular
    Returns:
        str: the pluralised version of the word
    """
    if count <= 1: 
        return word
    
    if word[-1] == 'y':
        return word[:-1] + 'ies'
    
    return word + "s"
    
def typeof(obj: any) -> str:
    """
    Returns the type of the object as a string.

    Args:
        obj (any): the object

    Returns:
        str: the type of the object
    """
    return type(obj).__name__

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