from argparse import ArgumentParser
from argcomplete import autocomplete
from argcomplete.completers import FilesCompleter
from lib.registry import Registry


# TODO -- Make the autocompletion case insensitive

class Parser: 
    """
    An argument parser for navigator. 
    Creating an instance sets all the required parsing and autocompletion options, and *parses* the arguments. 
    
    Attributes:
        args (argparse.Namespace): the arguments parsed
    """
    
    def __init__(self, registry: Registry | None = None):
        """
        Initialises the parser, sets the parsion and autocompletion options, and parses the arguments.

        Args:
            registry (Registry | None, optional): The registry which contains the list of available names one may navigate too; only used for autocompletion
        """
        registry = {  } if registry is None else registry
        
        parser = ArgumentParser(description="Manage and navigate to registered folders.")
        subparsers = parser.add_subparsers(dest="action")
        
        to_parser = subparsers.add_parser('to')
        to_parser.add_argument('name', choices=registry)
        
        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-a', '--all', action='store_true', dest='show_all')
        list_parser.add_argument('-b', '--broken', action='store_true', dest='show_broken')
        list_parser.add_argument('-i', '--invalid', action='store_true', dest='show_invalid')
        list_parser.add_argument('-p', '--path', action='store_true', dest='show_path')
        
        
        add_parser = subparsers.add_parser('add')
        add_parser.add_argument('name')
        add_parser.add_argument('path').completer = FilesCompleter()
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument('name', choices=registry|registry.broken|registry.invalid)
        
        doctor_parser = subparsers.add_parser("doctor")
        
        autocomplete(parser)
        self.args = parser.parse_args()

