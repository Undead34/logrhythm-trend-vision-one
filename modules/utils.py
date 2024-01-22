from .schemes.detections import DetectionsSchema
from .schemes.endpointActivityData import EndpointActivityData

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

def parse_OAT(output):
    print(f"Preparing to parse OAT detections...")
    type_detection = DetectionsSchema()
    type_endpointActivityData = EndpointActivityData()

    OATs = []

    for x in range(len(output["items"])):
        item = output["items"][x]

        if type_detection.isValid(item) and item.get("source") == "detections":
            detection = type_detection.parser(item)
            OATs.append(detection)
        elif type_endpointActivityData.isValid(item):
            endpointActivityData = type_endpointActivityData.parser(item)
            OATs.append(endpointActivityData)
        else:
            print(
                "Se ha encontrado un nuevo tipo de objeto. Hay que realizar el esquema."
            )
            # TODO: Realizar el esquema
            # print(item)

    print("Número de OATs: " + str(output["count"]))
    print("Número de OATs válidos: " + str(len(OATs)))
    print("Número de OATs inválidos: " + str(output["count"] - len(OATs)))
    return OATs