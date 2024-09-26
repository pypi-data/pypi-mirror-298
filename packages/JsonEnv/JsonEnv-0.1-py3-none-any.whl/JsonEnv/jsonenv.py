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

class Env():
    _instance = None
    path: str
    
    def __new__(cls, path: str):
        
        if cls._instance is None:
            cls._instance = super(Env, cls).__new__(cls)
            
            cls.__is_json(path)
            cls.__verify_path(path)
            
            cls._instance.path = path
        
        return cls._instance
    
    @staticmethod
    def __is_json(path: str):
        
        if not path.endswith(".json"):
            raise NotJsonFile("This file is not a .json")
    
    @staticmethod
    def __verify_path(path: str):
        
        if not os.path.exists(path):
            
            with open(path, 'w') as file:
                file: TextIOWrapper
                
                json.dump({"env" : {}}, file, indent=4)
                
            return
        
        with open(path, 'r') as file:
            
            data: str = file.read()
            
            if bool(data):
                
                if json.loads(data).get('env', None) is None:
                    raise NotEnv("The file does not have the env key")
                
                return
            
            raise EmptyFile("The file is empty")
    
    def get(self, key: str) -> any:
        
        with open(self.path, 'r') as env:
            return json.loads(env.read())['env'].get(key, None)
    
    def get_env(self) -> dict:
        
        with open(self.path, 'r') as env:
            
            return json.loads(env.read())['env']