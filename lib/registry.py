import json
from enum import Enum

from lib.misc import abspath, dir_exists

class RegistryStatus(Enum):
    """
    The possible status when initialising a Registry from a filename.
    """
    SUCCESS = 1 # The file could be read
    NO_FILE = 2 # The file does not exist
    NO_READ = 3 # The file exists but does not correspond to json format
    PARTIAL = 4 # The file exists and corresponds to json format, but the key-values are not all of type (str, str)

class Registry(dict[str, str]):
    """
        Registry extends dict[str, str] and is intended to store paths (values) under names (keys). 
        When registering a path under a certain name, this path is transformed into an absolute path.

        Attributes:
        status (RegistryStatus): the status of the initialisation from the source
        invalid (dict): the pairs of name-path (key-value) in the source which do not correspond to key-values pairs of type (str, str)
        broken (dict): the pairs of name-path (key-value) in the source for which path is not a valid directory

        Methods:
        contains: check if the Registry contains a name-path (key-value) pair after making path absolute 
    """
    def __init__(self, source: str | None = None):
        """
        
        Initialises the Registry from a mapping if given. 
        Will raise an error if the mapping is not a dict[str, str]
        
        Args:
            source (str | None, optional): name of the json file from which to to initialise the registry
        """
        super().__init__()
        self.status = RegistryStatus.SUCCESS
        self.invalid = {  }
        self.broken = {  }
        if source is None: return
        try:
            with open(source, 'r') as jsonfile:
                mapping = json.load(jsonfile)
        except FileNotFoundError: 
            mapping = {}
            self.status = RegistryStatus.NO_FILE
        except json.JSONDecodeError: 
            mapping = {}
            self.status = RegistryStatus.NO_READ
        finally:
            for k, v in mapping.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    self.status = RegistryStatus.PARTIAL
                    self.invalid[k] = v
                elif not dir_exists(v): 
                    self.status = RegistryStatus.PARTIAL
                    self.broken[k] = v
                else: self[k] = v
    
    def __setitem__(self, name: str, path: str) -> None:
        """
        Inserts or updates the key-value pair (name, path) in the registry.

        Args:
            name (str): key to register
            path (str): value registered for the key <name>

        Raises:
            TypeError: name and path both need to be instances of (str)
        """
        if not isinstance(name, str) and not isinstance(path, str):
            raise TypeError(f"Registry objects expects keys and values of type string but received name={name} (of type {type(name)}) and path={path} (of type {type(path)}).")
        if not isinstance(name, str): 
            raise TypeError(f"Registry objects expects keys of type string but received name={name} of type {type(name)}.")        
        if not isinstance(path, str): 
            raise TypeError(f"Registry objects expects values of type string but received path={path} of type {type(path)}.")
        formatted_path = abspath(path)
        super().__setitem__(name, formatted_path) 
        
    def contains(self, name: str, path: str) -> bool:
        """
        Checks if a key-value pair appears in the registry *after* transforming the path.
        Returns False instead of raising an error if name or path is not an instance of str.
        
        Args:
            name (str): the key for which we wish to check the value 
            path (str): the value to be checked against after making it absolute

        Returns:
            bool: whether the path associated with name is path
        """
        if not isinstance(name, str) or not isinstance(path, str): return False
        return name in self and self[name] == abspath(path)

    def write_to(self, filename: str) -> None:
        """
        Writes the current registry as a standard json file. 

        Args:
            filename (str): name of the file to write to
        """
        with open(filename, 'w') as file: json.dump(self | self.broken | self.invalid, file, indent=2)
    
    def _init_from(self, source: dict | str) -> None:
        """
        Helper function to initialise from a non-None source.

        Args:
            source (dict | str): the mapping (dictionary, json string or json filename) to initialise from
        """
        # TODO: handle the case where we do not succeed in importing from the source