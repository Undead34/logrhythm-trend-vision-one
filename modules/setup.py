from os import path
import os

from .constants import paths
from .loggers import console

def isfirstStart():
    firstStart = False
    
    firstStart |= not path.exists(paths["logs"])
    firstStart |= not path.exists(paths["oat"])

    return firstStart

def setup():
    console.debug("Configurando Trend Vision One...")
    os.makedirs(paths["logs"], exist_ok=True)
    os.makedirs(paths["oat"], exist_ok=True)