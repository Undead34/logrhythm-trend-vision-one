import logging.handlers as handlers
import logging
import json
import os

from utils.constants import paths
from utils import size_text_to_bytes


class Writer():
    def __init__(self) -> None:
        max_file_size = size_text_to_bytes(
            os.environ.get("MAX_FILE_SIZE") or "8MB")
        max_num_files = int(os.environ.get("MAX_NUM_FILES") or "50")

        # Configure Workbench Logger
        self.workbench_logger = logging.getLogger("workbench")
        output_path = os.path.join(paths.get("workbench"), "events.log")
        self.configure_logger(self.workbench_logger,
                              output_path, max_file_size, max_num_files)

        # Configure Audit Logs Logger
        self.audit_logs_logger = logging.getLogger("audit_logs")
        output_path = os.path.join(paths.get("audit_logs"), "events.log")
        self.configure_logger(self.audit_logs_logger,
                              output_path, max_file_size, max_num_files)

        # Configure OAT
        self.OAT_logger = logging.getLogger("OAT")
        output_path = os.path.join(paths.get("OAT"), "events.log")
        self.configure_logger(self.OAT_logger, output_path,
                              max_file_size, max_num_files)

        # Configure Detections
        self.detections_logger = logging.getLogger("detections")
        output_path = os.path.join(paths.get("detections"), "events.log")
        self.configure_logger(self.detections_logger,
                              output_path, max_file_size, max_num_files)

    def write(self, logs: list[str], stream):
        logger = None

        if stream == "workbench":
            logger = self.workbench_logger
        elif stream == "audit_logs":
            logger = self.audit_logs_logger
        elif stream == "OAT":
            logger = self.OAT_logger
        elif stream == "detections":
            logger = self.detections_logger

        try:
            for x in range(len(logs)):
                logger.info(logs[x])
        except Exception as e:
            try:
                print(json.dumps(logs, indent=4))
            except Exception as e:
                print(e)

    def configure_logger(self, logger: logging.Logger, log_file: str, max_size: int, max_files: int):
        logger.setLevel(logging.DEBUG)
        file_handler = handlers.RotatingFileHandler(
            log_file, maxBytes=max_size, backupCount=max_files, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(file_handler)
