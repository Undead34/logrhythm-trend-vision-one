import logging.handlers as handlers
import logging
import os

from .constants import paths, config

class TrendMicroLogger():
    def __init__(self) -> None:
        self.logger = logging.getLogger("TrendMicroLogger")
        self.logger.setLevel(logging.DEBUG)
        self.log_folder = paths["oat"]
        self.log_file = os.path.join(self.log_folder, "trend_micro_oat.log")
        self.file_handler = handlers.RotatingFileHandler(self.log_file, maxBytes=config["logger"]["max_size"], backupCount=config["logger"]["max_files"])
        self.file_handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.file_handler)

    def log(self, message: str):
            self.logger.info(message)

class Console(logging.Logger):
    def __init__(self) -> None:
        super().__init__("console")
        self.setLevel(logging.DEBUG)
        self.file_handler = handlers.RotatingFileHandler(os.path.join(os.path.curdir, "schedule-task.log"), encoding="utf-8", maxBytes=1000000, backupCount=5)
        self.file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.addHandler(self.file_handler)

        # Print to console
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.addHandler(self.console_handler)

    def warn(self, message: str):
        self.warning(message)

console = Console()