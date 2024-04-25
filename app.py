#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# Check if Python version is 3.7 or higher
if not sys.version_info >= (3, 7):
    print("LogRhythm Intruder requiere Python 3.7 o superior.")
    sys.exit(1)

from utils.test import check_environ_vars, check_permisions, check_first_start, check_connection
from modules.setup import setup
from modules.api import API
from modules.save import Writer
from utils import logs_cleanup


def bootstrap():
    check_environ_vars()

    if check_first_start():
        setup()
    else:
        check_permisions()

    check_connection()
    logs_cleanup()

    api = API(mode="stream")
    data = api.collect_data()

    w = Writer()
    w.write(data.get("workbench"), stream="workbench")
    w.write(data.get("OAT"), stream="OAT")
    w.write(data.get("audit_logs"), stream="audit_logs")
    # w.write(data.get("detections"), stream="detections")


# Main function
if __name__ == "__main__":
    try:
        bootstrap()
    except Exception as e:
        print(e)
        sys.exit(1)
