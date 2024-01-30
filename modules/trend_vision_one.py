from datetime import datetime, timezone, timedelta
import requests, json

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
        # self.getDetectionData()

    def getDetectionData(self):
        console.debug("Comenzando la obtención de Detection Data events...")

        query_params = {
            "startDateTime": self._getSegDiff(config["oat"]["timedelta"]),
            "endDateTime": self._getSegDiff(0),
            "top": config["oat"]["top"],
            "select": "empty",
            "mode": "default",
        }

        headers = {"TMV1-Query": "YOUR_QUERY (string)"}

        events = self._fetchTrendAPI(
            "/v3.0/search/detections", query_params=query_params, headers=headers
        )

        if isinstance(events, dict):
            print(json.dumps(events, indent=4))
        else:
            print(events)

    def getObservedAttackTechniques(self):
        try:
            console.debug(
                "Comenzando la obtención de Observed Attack Techniques events..."
            )

            query_params = {
                "detectedStartDateTime": self._getSegDiff(config["oat"]["timedelta"]),
                "detectedEndDateTime": self._getSegDiff(0),
                "top": config["oat"]["top"],
            }

            headers = {
                "TMV1-Filter": "(riskLevel eq 'low') or (riskLevel eq 'medium') or (riskLevel eq 'high') or (riskLevel eq 'critical')",  # Filtros
            }

            events = self._fetchTrendAPI(
                "/v3.0/oat/detections", query_params=query_params, headers=headers
            )
            logs = parseOATEvents(events)

            console.debug("Saving OAT detections...")
            for log in logs:
                self.logger.oat(log)

            console.debug("Tarea completada.")
        except Exception as e:
            console.error(e)

    def _fetchTrendAPI(self, url_path: str, query_params: dict = {}, headers: dict = {}):
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

            if "application/json" in r.headers.get("Content-Type", "") and len(
                r.content
            ):
                return r.json()
            else:
                return r.text
        except requests.Timeout as e:
            console.error("Timeout error:", e)
        except Exception as e:
            console.error(e)

    def _getSegDiff(self, seconds: int):
        diff: datetime = datetime.now(tz=timezone.utc) - timedelta(seconds=seconds)
        return diff.strftime("%Y-%m-%dT%H:%M:%SZ")