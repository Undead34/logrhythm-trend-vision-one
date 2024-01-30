from dotenv import load_dotenv
import os

from .utils import sizeTextToNum

# If no .env file is found, create copy from .env.example
if not os.path.exists(".env"):
    print("No se ha encontrado el archivo .env. Creando copia de .env.example...")
    with open(".env.example", "r") as f:
        with open(".env", "w") as f2:
            f2.write(f.read())

# Load .env file and override if already exists
load_dotenv(override=True)

config = {
    "api": {
        "token": os.environ.get("API_TOKEN"),
        "expiration": os.environ.get("EXPIRATION_DATE_TOKEN"),
        "region": os.environ.get("REGION"),
    },
    "smtp": {
        "email": os.environ.get("EMAIL"),
        "password": os.environ.get("EMAIL_PASSWORD"),
        "report_to": os.environ.get("EMAIL_REPORT"),
    },
    "logger": {
        "max_size": sizeTextToNum(os.environ.get("MAX_FILE_SIZE")) or sizeTextToNum("8MB"),
        "max_files": int(os.environ.get("MAX_NUM_FILES")) or 50,
    },
    "log_source_id": os.environ.get("LOG_SOURCE_ID"),
    "oat": {
        "timedelta": int(os.environ.get("OAT_TIMEDELTA")) or 300,
        "top": int(os.environ.get("OAT_TOP")) or 50,
    },
}

base_path = os.path.realpath(os.path.join(os.path.curdir, "logs"))
paths = {
    "logs": base_path,
    "oat": os.path.join(base_path, "Observed Attack Techniques"),
    "audit": os.path.join(base_path, "Audit Logs"),
    "detection": os.path.join(base_path, "Detection Data"),
    "workbench": os.path.join(base_path, "Workbench"),
}
