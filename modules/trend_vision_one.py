from os import path
import winreg
import shutil
import os

from datetime import datetime, timezone, timedelta
import requests

from .loggers import TrendMicroLogger, console
from .errors import AgentError
from .constants import config
from .utils import parse_OAT

class TrendVisionOne:
    def __init__(self):
        self.logger = TrendMicroLogger()

    def run(self):
        self._get_OAT()

    def _get_OAT(self):
        console.debug("Comenzando la obtención de OAT...")
        url_base = "https://api.xdr.trendmicro.com"
        url_path = "/v3.0/oat/detections"
        token = config["api"]["token"]

        query_params = {
            "detectedStartDateTime": (datetime.now(tz=timezone.utc) - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "detectedEndDateTime": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "top": 200,
        }

        headers = {
            "Authorization": "Bearer " + token,
            "TMV1-Filter": "",
        }

        r = requests.get(url_base + url_path, params=query_params, headers=headers)

        console.debug(r.status_code)
        for k, v in r.headers.items():
            console.debug(f"{k}: {v}")
        console.debug("")
        
        if "application/json" in r.headers.get("Content-Type", "") and len(r.content):
            output = r.json()
            console.debug(output.get("totalCount"))
            self._save_OAT(parse_OAT(output))
        else:
            console.debug(r.text)

        console.debug("Tarea completada.")

    def _save_OAT(self, OATs: list[str]):
        console.debug("Saving OAT detections...")
        for OAT in OATs:
            self.logger.log(OAT)