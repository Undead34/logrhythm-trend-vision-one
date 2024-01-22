from dotenv import load_dotenv
import os

from .utils import sizeTextToNum

# If no .env file is found, create copy from .env.example
if not os.path.exists(".env"):
    print("No se ha encontrado el archivo .env. Creando copia de .env.example...")
    with open(".env.example", "r") as f:
        with open(".env", "w") as f2:
            f2.write(f.read())

# Load .env file
load_dotenv(override=True)

config = {
    "api": {
        "token": os.environ.get("API_TOKEN"),
        "expiration": os.environ.get("EXPIRATION_DATE_TOKEN"),
        "region": os.environ.get("REGION"),
    },
    "email": {
        "report": os.environ.get("EMAIL_REPORT"),
        "alternative_report": os.environ.get("ALTERNATIVE_EMAIL_REPORT"),
        "email": os.environ.get("EMAIL"),
        "password": os.environ.get("EMAIL_PASSWORD"),
    },
    "logger": {
        "max_size": sizeTextToNum(os.environ.get("MAX_FILE_SIZE")),
        "max_files": int(os.environ.get("MAX_NUM_FILES")),  
    },
    "log_source_id": os.environ.get("LOG_SOURCE_ID"),
}

base_path = os.path.realpath(os.path.join(os.path.curdir, "logs"))
paths = {
    "logs": base_path,
    "oat": os.path.join(base_path, "OAT")
}
