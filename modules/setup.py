import os

from utils.constants import paths


def setup():
    print("It is the first start, creating directories")

    for _, value in paths.items():
        os.makedirs(value, exist_ok=True)
        print(f"The {value} directory has been created")
