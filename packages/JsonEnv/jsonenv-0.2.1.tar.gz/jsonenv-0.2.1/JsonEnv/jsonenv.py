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
    def load_env(cls, path: str):
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
        
        cls.__has_path(cls)
            
        with open(cls.__path, 'w') as wenv:
            
            data: dict = cls.__get_env()
            
            data[key] = value
            
            json.dump(data, wenv, indent=4)