# English

## What is JsonEnv?

JsonEnv is a Python library that allows you to use a json file to create environment variables, allowing you to directly save numbers, lists, booleans, etc. avoiding having to convert the environment variable (which is always returned as a string) to another data type.

### How to create an environment class:

```
from JsonEnv.jsonenv import Env

env: Env = Env("file_path.json")
```

### How to get the value of a key from the environment:

`env.get('key_name')`

### How to get all environment:

`env.get_env()`

# Español

## Que es JsonEnv?

JsonEnv es una libreria de Python que te permite usar un archivo json para crear variables de entorno, haciendo que puedas guardar directamente numeros, listas, booleanos, etc. evitando tener que convertir la variable de entorno (que siempre son devueltas como cadena) a otro tipo de dato.

### Como crear una clase de entorno:

```
from JsonEnv.jsonenv import Env

env: Env = Env("ruta_de_archivo.json")
```

### Como conseguir el valor de una llave de entorno:

`env.get('nombre_de_la_llave')`

### Como conseguir todo el entorno:

`env.get_env()`