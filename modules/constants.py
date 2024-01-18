from dotenv import load_dotenv
from os import path
import os

from .utils import sizeTextToNum

# Load .env file
load_dotenv(override=True)

config = {
    "api": {
        "token": os.environ.get("API_TOKEN"),
        "expiration": os.environ.get("EXPIRATION_DATE_TOKEN"),
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
    "region": os.environ.get("REGION"),
}

base_path = path.realpath(path.join(path.curdir, "logs"))
paths = {
    key: path.realpath(path.join(base_path, key))
    for key in ["oat"]
}
paths["logs"] = base_path
