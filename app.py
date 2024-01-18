#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timezone

from modules.constants import config
from modules.errors import TokenExpiredError, TokenNotSetError
from modules.loggers import Console
from modules.setup import isfirstStart, setup
from modules.tests import test
from modules.trend_vision_one import TrendVisionOne

console = Console()

def run():
    console.debug("Iniciando Trend Vision One...")
    trend_vision_one = TrendVisionOne()
    trend_vision_one.run()

def bootstrap():
    # Check if API_TOKEN is set
    if not config["api"]["token"] or config["api"]["token"] == "":
        raise TokenNotSetError()
    
    if config["api"]["expiration"] and config["api"]["expiration"] != "":
        dateformat = "%Y-%m-%dT%H:%M:%S.%fZ"
        expiration = datetime.strptime(config["api"]["expiration"], dateformat)
        expiration = expiration.astimezone(timezone.utc)
        today = datetime.now(timezone.utc)

        console.debug(f"La fecha de expiración del token es: {expiration}")
        console.debug(f"La fecha actual es: {today}")

        # If expiration date is less than current date, the token has expired
        if expiration < today:
            console.error("El token de Trend Vision One ha expirado.")
            raise TokenExpiredError()
        elif expiration <= (today + datetime.timedelta(days=7)): # If expiration date is less than current date + 7 days, the token will expire soon
            console.warn("Por favor, actualice el token en el archivo de configuración. (.env)\n"
            "Para obtener su token, vaya al siguiente enlace: https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys\n",
            "El token de Trend Vision One expirará en menos de 7 días.")
    else:
          console.warn("Advertencia: No se ha establecido una fecha de expiración para el token de Trend Vision One.")
          console.warn("Si no establece una fecha de expiración, el sistema no podrá notificarle cuando el token expire.")
    
    if isfirstStart(): setup(); run()
    else:
        if test():
            console.debug("Trend Vision One está listo para funcionar.")
            run()
        else:
            raise Exception("No se ha podido iniciar Trend Vision One. Los tests han fallado.")

if __name__ == "__main__":
    try:
        bootstrap()
    except Exception as e:
        console.error(e)
        sys.exit(1)
