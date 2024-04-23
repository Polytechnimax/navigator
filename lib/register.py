import json

from lib.misc import abspath

class Register(dict):
    
    def __init__(self, source=None):
        super().__init__()
        if source: self._init_from(source)
    
    def __setitem__(self, name: str, path: str):
        if not isinstance(name, str) and not isinstance(path, str):
            raise TypeError(f"Register objects expects keys and values of type string but received name={name} (of type {type(name)}) and path={path} (of type {type(path)}).")
        if not isinstance(name, str): 
            raise TypeError(f"Register objects expects keys of type string but received name={name} of type {type(name)}.")        
        if not isinstance(path, str): 
            raise TypeError(f"Register objects expects values of type string but received path={path} of type {type(path)}.")
        formatted_path = abspath(path)
        super().__setitem__(name, formatted_path) 
    
    def contains(self, name: str, path=None):
        if not isinstance(name, str): return False
        if path == None: return name in self
        if not isinstance(path, str): return False
        return name in self and self[name] == abspath(path)

    def write_to(self, filename: str):
        with open(filename, 'w') as file: json.dump(self, file, indent=2)
    
    def _init_from(self, source):
        if isinstance(source, dict):
            for k, v in source.items(): self[k] = v
            return
        if isinstance(source, str):
            try: 
                with open(source, 'r') as file: 
                    mapping = json.load(file)
                    for k, v in mapping.items(): self[k] = v
                return
            except: pass
            try:
                mapping = json.loads(source)
                for k, v in mapping.item(): self[k] = v
                return 
            except: pass            
        # TODO: handle the case where we do not succeed in importing from the source
    
     
        
if __name__ == "__main__":
    FILENAME = "navigator_conf_tests/navconf.json"    
    register = Register( FILENAME )
    # register['documents'] = '~/Documents/'
    # register['WoRk'] = "~/Documents/Work/"
    # register['here-auto'] = '.'
    print(register)
    # register.write_to( FILENAME )
