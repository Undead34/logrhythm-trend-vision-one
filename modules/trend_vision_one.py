from datetime import datetime, timezone, timedelta
import requests

from .loggers import TrendMicroLogger, console
from .constants import config
from .parsers import parse_OAT
from .utils import getRegion

class TrendVisionOne:
    def __init__(self):
        self.logger = TrendMicroLogger()
        self._getOATLogs()

    # Muestra una lista de eventos de técnicas de ataque observadas que coinciden con los criterios especificados.
        
    def _getOATLogs(self):
        try:
            console.debug("Comenzando la obtención de Observed Attack Techniques events...")
            url_base = "https://" + getRegion(config["api"]["region"])
            url_path = "/v3.0/oat/detections"
            token = config["api"]["token"]

            query_params = {
                "detectedStartDateTime": (datetime.now(tz=timezone.utc) - timedelta(minutes=8)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "detectedEndDateTime": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "top": 100,
            }

            headers = {
                "Authorization": "Bearer " + token,
                "TMV1-Filter": "(riskLevel eq 'critical')", # Filtros
            }

            r = requests.get(url_base + url_path, params=query_params, headers=headers)

            console.debug(r.status_code)
            for k, v in r.headers.items():
                console.debug(f"{k}: {v}")
            console.debug("")
            
            if "application/json" in r.headers.get("Content-Type", "") and len(r.content):
                output = r.json()
                console.debug(output.get("totalCount"))
                logs = parse_OAT(output)

                console.debug("Saving OAT detections...")
                for log in logs:
                    self.logger.oat(log)
            else:
                console.debug(r.text)
            
            console.debug("Tarea completada.")
        except Exception as e:
            console.error(e)