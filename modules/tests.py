import requests
import json
import os

from .constants import config, paths
from .loggers import console
from .errors import NetworkError, FileSystemError

def _network_test():
    try:
        console.debug("Comprobando conexión con Trend Vision One...")
        url_base = "https://api.xdr.trendmicro.com"
        url_path = "/v3.0/healthcheck/connectivity"
        token = config["api"]["token"]

        query_params = {}
        headers = {"Authorization": "Bearer " + token}

        r = requests.get(url_base + url_path, params=query_params, headers=headers)
        message = ""
        message += f"Status Code: {r.status_code}\n"

        for k, v in r.headers.items():
            message += f"{k}: {v}\n"
        
        if "application/json" in r.headers.get("Content-Type", "") and len(r.content):
            message += json.dumps(r.json(), indent=4)
        else:
            message += r.text
        
        # print(message)

        if r.status_code == 401:
            raise NetworkError(
                "[URGENTE]!!! El token de Trend Vision One ha expirado o no es válido.\n"
                "Por favor, actualice el token en el archivo de configuración. (.env)\n"
                "\n"
                "No se ha podido iniciar sesión en el servidor de Trend Vision One.\n"
                "Por favor, compruebe que el token es correcto.\n"
                "\n"
                "DETALLES:\n"
                f"{message}"
            )
        elif r.status_code != 200:
            print(message)
        else:
            return True
    except NetworkError as e:
        raise e
    except Exception as e:
        raise NetworkError("No se ha podido establecer conexión con Trend Vision One.\nPor favor, compruebe su conexión a Internet.")
    return False

def _paths_test():
    try:
        console.debug("Comprobando directorios necesarios para el funcionamiento de Trend Vision One...")
        for key, value in paths.items():
            if not os.path.exists(value):
                raise FileSystemError(f"El directorio {key} no existe.")
            if not os.path.isdir(value):
                raise FileSystemError(f"El directorio {key} no es un directorio.")
            if not os.access(value, os.W_OK):
                raise FileSystemError(f"El directorio {key} no tiene permisos de escritura.")
    except FileSystemError as e:
        raise e
    except Exception as e:
        raise FileSystemError("No se han podido crear los directorios necesarios para el funcionamiento de Trend Vision One.")
    return True

def test():
    try:
        _network_test()
        _paths_test()
        return True
    except NetworkError as e:
        console.debug("NetworkError in test function")
        e.report()
    except FileSystemError as e:
        console.debug("FileSystemError in test function")
        e.report()
    except Exception as e:
        console.error(e.message)
    
    return False
