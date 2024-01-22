import logging.handlers as handlers
import logging
import os

from .constants import paths, config

class TrendMicroLogger():
    def __init__(self) -> None:
        self.oat_logger = logging.getLogger("oat")
        oat_log_file = os.path.join(paths.get("oat"), "oat.log")
        self.configure_logger(self.oat_logger, oat_log_file, config[""][""], config[""][""])

    def oat(self, message: str):
        self.oat_logger.info(message)

    def configure_logger(logger: logging.Logger, log_file: str, max_size: int, max_files: int):
        logger.setLevel(logging.DEBUG)
        file_handler = handlers.RotatingFileHandler(log_file, maxBytes=max_size, backupCount=max_files)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(file_handler)

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