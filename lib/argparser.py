from argparse import ArgumentParser
from argcomplete import autocomplete
from argcomplete.completers import FilesCompleter

# TODO -- Make the autocompletion case insensitive

class Parser: 
    def __init__(self, register=None):
        register = {  } if register is None else register
        
        parser = ArgumentParser(
        description="Manage and navigate to registered folders."
        )
        subparsers = parser.add_subparsers(dest="action")
        
        to_parser = subparsers.add_parser('to')
        to_parser.add_argument('name', choices=register)
        
        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-p', '--path', action='store_true', dest='show_path')
        
        add_parser = subparsers.add_parser('add')
        add_parser.add_argument('name')
        add_parser.add_argument('path').completer = FilesCompleter()
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument('name', choices=register)
        
        doctor_parser = subparsers.add_parser("doctor")
        
        autocomplete(parser)
        self.args = parser.parse_args()

