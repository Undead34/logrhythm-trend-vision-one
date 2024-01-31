import requests, json

from .loggers import TrendMicroLogger, console
from .constants import config
from .parsers import parseOATEvents
from .utils import get_region, get_deltatime

"""
    Clase que se encarga de obtener los eventos arronjados por Trend Vision One
    y guardarlos en el archivo de logs.
"""


class TrendVisionOne:
    def __init__(self):
        self.logger = TrendMicroLogger()
        self.url_base = "https://" + get_region(config["api"]["region"])
        self.token = config["api"]["token"]

        # Get events
        oat_start = get_deltatime(config["oat"]["timedelta"])
        oat_end = get_deltatime(0)
        oat_top = config["oat"]["top"]
        self.get_oat(oat_start, oat_end, oat_top)

        # self.get_detection()
        # self.get_audit_logs()

    def get_oat(self, start, end, top):
        console.debug("Obteniendo logs de Observed Attack Techniques events...")

        params = {}
        if start is not None:
            params["detectedStartDateTime"] = start
        if end is not None:
            params["detectedEndDateTime"] = end
        if top is not None:
            params["top"] = top

        headers = {
            "TMV1-Filter": "(riskLevel eq 'low') or (riskLevel eq 'medium') or (riskLevel eq 'high') or (riskLevel eq 'critical')"
        }

        oat = self.get_items("/v3.0/oat/detections", params=params, headers=headers)
        console.debug("Saving OAT detections...")
        logs = parseOATEvents(oat)
        for log in logs:
            self.logger.oat(log)

    def get_items(self, url_path, params=None, headers=None):
        items = []
        next_link = None
        totalCount = 0
        count = 0

        while True:
            if next_link is None:
                r = self.fetch(url_path, query_params=params, headers=headers)
            else:
                r = self.fetch(next_link, query_params=None, headers=headers)

            items.extend(r["items"])

            if "totalCount" in r:
                totalCount = r["totalCount"]
            
            if "count" in r:
                count += r["count"]

            if "nextLink" not in r:
                break

            next_link = r["nextLink"]

        return {
            "totalCount": totalCount,
            "count": count,
            "items": items
        }

    def fetch(self, url_or_path, query_params=None, headers=None, use_token=True):
        if query_params is None:
            query_params = {}
        if headers is None:
            headers = {}

        if use_token:
            headers["Authorization"] = "Bearer " + self.token

        url_path = None

        if url_or_path.startswith("/"):
            url_path = self.url_base + url_or_path
        else:
            url_path = url_or_path

        r = requests.get(url_path, params=query_params, headers=headers)

        if 200 == r.status_code:
            if "application/json" in r.headers.get("Content-Type", ""):
                return r.json()
            return r.content

        raise RuntimeError(
            f"Request unsuccessful (GET {url_path}):" f" {r.status_code} {r.text}"
        )

    @staticmethod
    def checkAPIStatus() -> bool:
        url_base = "https://" + get_region(config["api"]["region"])
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

        return r.status_code, message
