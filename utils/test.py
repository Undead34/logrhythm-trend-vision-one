import json
import requests
from dotenv import load_dotenv
import sys
import os
from utils.dateutils import parse_ISO_8601, get_left_days
from utils.constants import paths, logs_ids
from utils import get_region


def check_environ_vars():
    # Load .env file and override if already exists
    load_dotenv(override=True)

    region = os.environ.get("REGION").upper()

    # Regions: India, Japan, Singapore, United States, United States (for Government)
    if region not in ["AU", "EU", "IN", "JP", "SG", "US", "USGOV"]:
        print("An invalid region has been detected, please check your .env file, the program will try to continue using US")
        region = "US"

    os.environ["REGION"] = region

    api_token = os.environ.get("API_TOKEN")

    if not api_token or api_token == "":
        print("The token was not found. Please edit the .env file to add it.")
        sys.exit(1)

    expiration_date_token = os.environ.get("EXPIRATION_DATE_TOKEN")

    if expiration_date_token.lower() == "infinity":
        print("The token has no expiration date.")
    elif not expiration_date_token or expiration_date_token == "":
        print("No expiration date was set for the token, the tool will not be able to warn you when the token is about to expire.")
    else:
        expiration_date_token = parse_ISO_8601(expiration_date_token)

        if not expiration_date_token:
            print(
                "The date I put in the EXPIRATION_DATE_TOKEN field is not in the correct format please check it")
        else:
            expiration = get_left_days(expiration_date_token)

            if expiration <= 0:
                print("The token has expired, please update the token.")
                sys.exit(1)
            elif expiration <= 7 and expiration > 0:
                print(
                    f"The token will expire soon with {expiration} days left.")
            else:
                print(
                    f"There are {expiration} days left for the token to expire, when there are less than 7 days left we will warn you.")

    log_sources = os.environ.get("LOG_SOURCES_ID")

    if log_sources is None:
        print("LOG_SOURCES_ID is not set")
    


def check_permisions():
    try:
        for _, path in paths.items():
            if not os.path.exists(path) or not os.path.isdir(path):
                print(
                    f"The path {path} does not exist or it is not a directory")

                sys.exit(1)
            if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
                print(f"The program does not have permissions to access the resources.")

                sys.exit(1)

            print(f"The path {path} is a directory and can be accessed by")
    except Exception as e:
        print(e)
        sys.exit(1)


def check_first_start():
    firstStart = False

    for _, value in paths.items():
        if not os.path.exists(value):
            firstStart = True
            break

    return firstStart


def check_connection():
    try:
        region = os.environ.get("REGION")
        api_token = os.environ.get("API_TOKEN")

        url_base = "https://" + get_region(region)
        url_path = "/v3.0/healthcheck/connectivity"

        headers = {"Authorization": "Bearer " + api_token}

        r = requests.get(url_base + url_path, params={}, headers=headers)
        status_code = r.status_code

        message = ""
        message += f"Status Code: {status_code}\n"

        for k, v in r.headers.items():
            message += f"{k}: {v}\n"

        status = None

        if "application/json" in r.headers.get("Content-Type", "") and len(r.content):
            status = r.json().get("status") or 'Unauthorized'
            message += status
        else:
            message += r.text

        if status_code != 401 and (not status or status != "available"):
            print("The XDR API is not available.")
            sys.exit(0)

        if status_code == 401:
            print("The token has expired, please update the token.")
            sys.exit(0)
        elif status_code != 200:
            print(message)
        else:
            print("Connection established.")
    except Exception as e:
        print(e)
        sys.exit(1)
