import json, os
from io import TextIOWrapper

class NotJsonFile(Exception):

    def __init__(self, args):
        super().__init__(args)

class NotEnv(Exception):
    
    def __init__(self, args):
        super().__init__(args)

class EmptyFile(Exception):
    
    def __init__(self, args):
        super().__init__(args)

class ConstPath(Exception):
    
    def __init__(self, args):
        super().__init__(args)

class UnassignedPath(Exception):
    
    def __init__(self, args):
        super().__init__(args)

class env():
    __path: str = None
    
    @classmethod
    def load(cls, path: str):
        """Load a file how a env

        Args:
            path (str): File Path

        Raises:
            ConstPath: Only if the path is not None
        """
        if cls.__path is None:
            cls.__is_json(path)
            cls.__verify_path(path)
            cls.__path = path  # Asigna el path
            return
        
        raise ConstPath("The path cannot be changed.")
    
    @staticmethod
    def __is_json(path: str):
        
        if not path.endswith(".json"):
            raise NotJsonFile("This file is not a .json")
    
    @staticmethod
    def __verify_path(path: str):
        
        if not os.path.exists(path):
            
            with open(path, 'w') as file:
                file: TextIOWrapper
                
                json.dump({
                    "env" : {
                        
                    }
                }, file, indent=4)
                
            return
        
        with open(path, 'r') as file:
            
            data: str = file.read()
            
            if bool(data):
                
                if json.loads(data).get('env', None) is None:
                    raise NotEnv("The file does not have the env key")
                
                return
            
            raise EmptyFile("The file is empty")
    
    def __has_path(cls):
        
        if cls.__path is None:
            raise UnassignedPath("The path is not assignet")
    
    @classmethod
    def get(cls, key: str) -> any:
        """Get a value of a key of the env

        Args:
            key (str): Env key

        Returns:
            any: The value of the key
        """
        
        cls.__has_path(cls)
        
        with open(cls.__path, 'r') as env:
            return json.loads(env.read())['env'].get(key, None)
    
    @classmethod
    def __get_env(cls) -> dict:
        
        cls.__has_path(cls)
        
        with open(cls.__path, 'r') as env:
            return json.loads(env.read())
    
    @classmethod
    def change(cls, key: str, value: any):
        """Change a value of a key

        Args:
            key (str): Env key
            value (any): New value
        """
        
        cls.__has_path(cls)
        
        data: dict = cls.__get_env()
        data['env'][key] = value
            
        with open(cls.__path, 'w') as wenv:
            json.dump(data, wenv, indent=4)
    
    @classmethod
    def get_change(cls, key: str, value: any):
        """Return a key value, and after change the key value

        Args:
            key (str): Env Key
            value (any): New value for the key
        """
        
        getter: any = cls.get(key)
        cls.change(key, value)
        
        return getter