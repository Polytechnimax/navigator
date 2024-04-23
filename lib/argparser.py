import argparse

class Parser: 
    def __init__(self):
        parser = argparse.ArgumentParser(
        description="Manage and navigate to registered folders."
        )
        subparsers = parser.add_subparsers(dest="action")
        
        to_parser = subparsers.add_parser('to')
        to_parser.add_argument('name')
        
        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-p', '--path', action='store_true', dest='show_path')
        
        add_parser = subparsers.add_parser('add')
        add_parser.add_argument('name')
        add_parser.add_argument('path')
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument('name')
        
        doctor_parser = subparsers.add_parser("doctor")
        
        self.args = parser.parse_args()

