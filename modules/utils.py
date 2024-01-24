from datetime import datetime, timezone

def sizeTextToNum(size: str):
    """Converts a size string to a number of bytes
    Args:
        size (str): The size string to convert
    Returns:
        int: The number of bytes
    """
    size = size.upper()

    if size and size[-1] == "B":
        size = size[:-1]
    if size and (size[-1] == "K" or size[-2:] == "KB"):
        return int(float(size[:-1]) * 1000)
    elif size and (size[-1] == "M" or size[-2:] == "MB"):
        return int(float(size[:-1]) * 1000 * 1000)
    elif size and (size[-1] == "G" or size[-2:] == "GB"):
        return int(float(size[:-1]) * 1000 * 1000 * 1000)
    else:
        return int(size)

def getISO8601Time():
    return datetime.now().isoformat()

# return URL for region by region code e.g "US" -> "api.xdr.trendmicro.com"
def getRegion(code: str):
    if code == "AU":
        return "api.au.xdr.trendmicro.com"
    elif code == "EU":
        return "api.eu.xdr.trendmicro.com"
    elif code == "IN":
        return "api.in.xdr.trendmicro.com"
    elif code == "JP":
        return "api.xdr.trendmicro.co.jp"
    elif code == "SG":
        return "api.sg.xdr.trendmicro.com"
    elif code == "US":
        return "api.xdr.trendmicro.com"
    elif code == "USGOV":
        return "api.usgov.xdr.trendmicro.com"
    else:
        return "api.xdr.trendmicro.com"

def getTokenDays(expiration: str):
    """Returns the number of days until the token expires
    Args:
        token (str): The token to check
    Returns:
        int: The number of days until the token expires
    """
    try:
        expiration = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S.%fZ")
        expiration = expiration.astimezone(timezone.utc)
        today = datetime.now(timezone.utc)
        return (expiration - today).days
    except:
        return 0
