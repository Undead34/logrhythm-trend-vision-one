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
        self._cleanup()
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

    def _cleanup(self):
        console.debug("Comezando la limpieza...")
        
        # In this folder we can find many .pos files.
        # X:\LogRhythm\LogRhythm System Monitor\state\[ID]
        agent_state = self._get_agent_state()
        log_source_pos_dir = f"{agent_state}state\\{config['log_source_id']}"
        self.move_completed_files(log_source_pos_dir, config["paths"]["archived"])
        console.debug("Limpieza completada.")

    def _save_OAT(self, OATs: list[str]):
        console.debug("Saving OAT detections...")
        for OAT in OATs:
            self.logger.log(OAT)

    # Getting Agent state location from registry.
    def _get_agent_state(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\LogRhythm\scsm")
            agent_state, _ = winreg.QueryValueEx(key, "STATEPATH")
            return agent_state
        except FileNotFoundError:
            raise AgentError(
                "No se pudo encontrar la ubicación del estado del agente.\nPor favor, asegúrese de que el agente esté instalado."
            )
        except Exception as e:
            console.error(f"Type: {type(e)}\n{e.message}")

    def _move_completed_files(self, pos_dir, archive_path):
        file_count = 0

        # Pos file example content:
        # X:\path\to\vision_one.log
        # 12478343
        # 638408987240279906

        for file in os.listdir(pos_dir):  # Iterate through all files in the directory
            with open(path.join(pos_dir, file), "r") as f:  # Open the file
                file_info = f.read().split("\n")  # file_info = [path, number, number]

            if path.exists(file_info[0]):  # Check if the file exists
                if path.getsize(file_info[0]) == int(file_info[1]):  # Check if the file size is equal to the size in the .pos file
                    dest_fname = path.basename(file_info[0])
                    shutil.move(file_info[0], path.join(archive_path, dest_fname))
                    console.debug(
                        f"Read of {file_info[0]} complete. Moved to {path.join(archive_path, dest_fname)}"
                    )
                    file_count += 1

        console.debug(f"{file_count} files moved.")
