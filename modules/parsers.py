from .schemes.endpointActivityData import EndpointActivityData
from .schemes.detections import DetectionsSchema
from .loggers import console
import json

def parse_OAT(output):
    console.debug("Preparing to parse OAT detections...")
    totalCount = output.get("totalCount")
    count = output.get("count")
    items = output.get("items")
    OATs = []

    if count < totalCount:
        console.warn(f"There are more detections than the ones shown. Please, increase the 'top' parameter. (Current: {count}, Total: {totalCount})")

    for i in range(len(items)):
        item = items[i]
        
        if item.get("source") == "detections":
            OATs.append(detections_OAT(item))

    return OATs

def detections_OAT(item):
    detection = ""

    # Principales
    detection += f"source: {str(item.get('source'))}#"
    detection += f"uuid: {str(item.get('uuid'))}#"
    detection += f"detectedDateTime: {str(item.get('detectedDateTime'))}#"
    detection += f"ingestedDateTime: {str(item.get('ingestedDateTime'))}#"
    detection += f"entityType: {str(item.get('entityType'))}#"
    detection += f"entityName: {str(item.get('entityName'))}#"

    detail = item.get("detail")

    # Detalles
    detection += f"objectFileName: {str(detail.get('objectFileName'))}#"
    detection += f"objectFilePath: {str(detail.get('objectFilePath'))}#"
    detection += f"objectFileSize: {str(detail.get('objectFileSize'))}#"
    detection += f"objectFileHashSha1: {str(detail.get('objectFileHashSha1'))}#"

    excludeKeys = [
        "objectFileName",
        "objectFilePath",
        "objectFileSize",
        "objectFileHashSha1",
        "filePath",
        "fileHash",
        "objectType",
        "ruleName",
        "malName",
        "eventName",
        "eventSubName",
        "fullPath",
        "eventId",
        "scanType",
        "malDst",
        "domainName",
        "malType",
        "firstActResult",
        "channel",
        "malFamily",
    ]

    for key in excludeKeys:
        detection += f"{key}: {str(detail.get('{key}'))}#"

    for key, value in detail.items():
        if (key not in excludeKeys):
            if isinstance(value, (str, bool, int, list)):
                detection += f"{key}: {str(value[0] if isinstance(value, list) and len(value) == 1 else value)}#"
            else:
                detection += f"{key}: {str(value)}#"
        return detection[:-1]


# type_detection = DetectionsSchema()
# type_endpointActivityData = EndpointActivityData()
# for x in range(len(output["items"])):
#     item = output["items"][x]

#     if type_detection.isValid(item) and item.get("source") == "detections":
#         detection = type_detection.parser(item)
#         OATs.append(detection)
#     elif type_endpointActivityData.isValid(item):
#         endpointActivityData = type_endpointActivityData.parser(item)
#         OATs.append(endpointActivityData)
#     else:
#         print(
#             "Se ha encontrado un nuevo tipo de objeto. Hay que realizar el esquema."
#         )
#         # TODO: Realizar el esquema
#         # print(item)
# print("Número de OATs: " + str(output["count"]))
# print("Número de OATs válidos: " + str(len(OATs)))
# print("Número de OATs inválidos: " + str(output["count"] - len(OATs)))