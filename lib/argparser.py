from argparse import ArgumentParser
from argcomplete import autocomplete
from argcomplete.completers import FilesCompleter, ChoicesCompleter
from lib.registry import Registry





# TODO -- Make the autocompletion case insensitive

class Parser: 
    """
    An argument parser for navigator. 
    Creating an instance sets all the required parsing and autocompletion options, and parses the arguments. 
    
    Attributes:
        args (dict[str, str | bool]): the arguments parsed
    """
    
    def __init__(self, registry: Registry | None = None):
        """
        Initialises the parser, sets the parsion and autocompletion options, and parses the arguments.

        Args:
            registry (Registry | None, optional): The registry which contains the list of available names one may navigate too; only used for autocompletion
        """
        registry = {  } if registry is None else registry
        
        parser = ArgumentParser(description="Navigate to and manage registered folders.")
        subparsers = parser.add_subparsers(dest="action")
        
        to_parser = subparsers.add_parser('to', description="Navigate with Terminal and Finder to name folder.")
        to_parser.add_argument('name', choices=registry, help="Name of the registered folder to navigate to.")
        
        list_parser = subparsers.add_parser('list', description="List available registered folders." )
        list_parser.add_argument('-a', '--all', action='store_true', dest='show_all', help="Also show broken and invalid entries.")
        list_parser.add_argument('-b', '--broken', action='store_true', dest='show_broken', help='Show only entries with broken paths (i.e. broken paths).')
        list_parser.add_argument('-i', '--invalid', action='store_true', dest='show_invalid', help='Show only entries with invalid paths (i.e. not paths).')
        list_parser.add_argument('-p', '--path', action='store_true', dest='show_path', help="Also display the paths.")
        
        
        add_parser = subparsers.add_parser('add', description="Add a folder to the registry.")
        add_parser.add_argument('path', help='Path to the folder.').completer = FilesCompleter()
        add_parser.add_argument('name', help='Name under which to save the folder.')

        del_parser = subparsers.add_parser("del", description="Deletes a folder from the registry.")
        del_parser.add_argument('name', help="Name of the folder to delete.").completer = ChoicesCompleter(choices = registry|registry.broken|registry.invalid)
        
        clean_parser = subparsers.add_parser("clean", description="Remove broken and invalid entries from the registry.")
        clean_parser.add_argument('-b', '--broken', action='store_true', dest='clean_broken', help="Remove only broken entries.")
        clean_parser.add_argument('-i', '--invalid', action='store_true', dest='clean_invalid', help="Remove only invalid entries.")
        
        doctor_parser = subparsers.add_parser("doctor", description="Not yet implemented.") # TODO
        
        autocomplete(parser)
        self.args = vars(parser.parse_args())

