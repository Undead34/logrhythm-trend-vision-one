# LogRhythm Flat File Trend Vision One

Esta herramienta te ayuda a configurar LogRhythm con Trend Vision One a través de `Flat File`.

## Comenzando
Actualmente esta herramienta solo funciona en Windows o bueno... no ha sido probada en Linux si logras hacerla funcionar en Linux recuerda enviar tu PR. Se un buen ser humano y respeta la licencia que es GPL :D

Para empezar a utilizar esta herramienta debes clonar este repositorio y colocarlo en donde quieras en tu servidor SIEM. El lugar donde lo coloques debe tener suficiente espacio para poder guardar logs. Recomendamos mínimo 5 GB. Aunque esta herramienta tiene un sistema de limpieza automático, es bueno tener espacio adicional.

Ejecuta este comando en tu terminal para clonar el repositorio:

    git clone --depth 1 https://github.com/Undead34/logrhythm-trend-vision-one.git

Luego crea una copia del archivo `.env.example` y renómbrala para `.env`. Aquí hay un ejemplo de como puedes configurar tu archivo `.env`

```Properties
# Regions:
    # Australia=AU
    # European Union=EU
    # India=IN
    # Japan=JP
    # Singapore=SG
    # United States=US
    # United States (for Government)=USGOV
REGION="US"

API_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...."

# YYYY = Year with century as a decimal number. e.g 2013
# mm = 	Month as a zero-padded decimal number. e.g  09
# dd = Day of the month as a zero-padded decimal number. e.g  10
# HH = 	Hour (24-hour clock) as a zero-padded decimal number. e.g 22
# MM = Minute as a zero-padded decimal number. e.g 59
# ss = Second as a zero-padded decimal number. e.g: 05
# ms = Microsecond as a decimal number, zero-padded to 6 digits. e.g: 000000
EXPIRATION_DATE_TOKEN="2013-09-10T22:59:05.000000Z" # YYYY-mm-ddTHH:MM:SS:msZ = 2013-09-10T22:59:05.000000Z

# These settings are used to report when an error occurs or when a warning is needed.
EMAIL_REPORT="jhondoe@example.com"
ALTERNATIVE_EMAIL_REPORT="janedoe@example.com"

# SMTP Settings
EMAIL="mailer@example.com"
EMAIL_PASSWORD="xxx...."

# N or NB or N(K,KB,M,MB,G,GB)
# N = Number of files
# N(K,KB,M,MB,G,GB) = Number of bytes in KiloBytes, MegaBytes, GigaBytes 
MAX_FILE_SIZE="10MB"
MAX_NUM_FILES="100"

# Enter the "Log Source ID". 
# This can be found by looking at the Log Source under the Log Sources tab in the console.
LOG_SOURCE_ID="0"
```

Luego de eso debes crear en entorno virtual de Python. Para eso necesitar tener instalado **Python 3.7** o superior, recomendamos **Python 3.10**.

En la terminal dentro del proyecto ejecuta:

Crear el entorno virtual:

    python -m vevn .venv
Activar el entorno virtual

    .\.venv\Scripts\activate
Instalar las dependencias de Python

    pip install -r requirements.txt

Si todo está funcionando correctamente debería crearse una carpeta `logs` y allí encontrarás los logs que llegan. Buena suerte.
