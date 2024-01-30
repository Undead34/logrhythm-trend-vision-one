from datetime import datetime, timezone, timedelta
import requests

from .loggers import TrendMicroLogger, console
from .constants import config
from .parsers import parseOATEvents
from .utils import getRegion

"""
    Clase que se encarga de obtener los eventos arronjados por Trend Vision One
    y guardarlos en el archivo de logs.
"""
class TrendVisionOne:
    def __init__(self):
        self.logger = TrendMicroLogger()
        self.getObservedAttackTechniques()

    def getObservedAttackTechniques(self):
        try:
            console.debug("Comenzando la obtención de Observed Attack Techniques events...")

            query_params = {
                "detectedStartDateTime": (datetime.now(tz=timezone.utc) - timedelta(seconds=config["oat"]["timedelta"])).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "detectedEndDateTime": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "top": config["oat"]["top"],
            }

            headers = {
                "TMV1-Filter": "(riskLevel eq 'low') or (riskLevel eq 'medium') or (riskLevel eq 'high') or (riskLevel eq 'critical')", # Filtros
            }

            events = self.fetchTrendAPI("/v3.0/oat/detections", query_params=query_params, headers=headers)
            logs = parseOATEvents(events)

            console.debug("Saving OAT detections...")
            for log in logs:
                self.logger.oat(log)
            
            console.debug("Tarea completada.")
        except Exception as e:
            console.error(e)

    def fetchTrendAPI(self, url_path: str, query_params: dict = {}, headers: dict = {}):
        try:
            url_base = "https://" + getRegion(config["api"]["region"])
            url_path = "/v3.0/oat/detections"
            token = config["api"]["token"]

            headers = {
                "Authorization": "Bearer " + token,
            }

            headers.update(headers)

            r = requests.get(url_base + url_path, params=query_params, headers=headers)

            console.debug(r.status_code)

            for k, v in r.headers.items():
                console.debug(f"{k}: {v}")
            console.debug("")

            if "application/json" in r.headers.get("Content-Type", "") and len(r.content):
                return r.json()
            else:
                return r.text
        except requests.Timeout as e:
            console.error("Timeout error:", e)
        except Exception as e:
            console.error(e)