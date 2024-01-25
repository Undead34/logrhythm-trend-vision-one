from .schemes.endpointActivityData import EndpointActivityData
from .schemes.detections import DetectionsSchema
from .loggers import console
import binascii
import json

# Example of endpointActivityData
# {
#   "source": "endpointActivityData",
#   "uuid": "5f72476a-2a77-4280-a8e8-c274b3326b82",
#   "detectedDateTime": "2024-01-25T15:12:04Z",
#   "filters": [
#     {
#       "id": "F1796",
#       "name": "Process Discovery",
#       "description": "List running process",
#       "highlightedObjects": [
#         {
#           "field": "processCmd",
#           "type": "command_line",
#           "value": "C:\\Windows\\system32\\cmd.exe /c \"\"C:\\biopagobdv\\autobiopago.bat\" \""
#         },
#         {
#           "field": "objectCmd",
#           "type": "command_line",
#           "value": "tasklist  /FI \"IMAGENAME eq biopago.exe\" /FO CSV "
#         }
#       ],
#       "mitreTacticIds": [
#         "TA0002",
#         "TA0007"
#       ],
#       "mitreTechniqueIds": [
#         "T1010",
#         "T1057",
#         "T1059",
#         "T1059.003"
#       ],
#       "riskLevel": "info",
#       "type": "preset"
#     }
#   ],
#   "detail": {
#     "endpointGuid": "cf9d0cf0-dfd5-4d21-8a0d-2d24e76d8cd0",
#     "endpointHostName": "CJ2605VE02",
#     "endpointIp": [
#       "fe80::816d:cdcf:e337:bd6c",
#       "172.16.214.22"
#     ],
#     "eventId": "1",
#     "eventSubId": 2,
#     "eventTime": "1706195524244",
#     "firstSeen": "1706195524244",
#     "integrityLevel": 12288,
#     "lastSeen": "1706195524244",
#     "logonUser": [
#       "UCJ2605VE02"
#     ],
#     "objectCmd": "tasklist  /FI \"IMAGENAME eq biopago.exe\" /FO CSV ",
#     "objectFileHashMd5": "d0a49a170e13d7f6aebbefed9df88aaa",
#     "objectFileHashSha1": "d61ffd641c2f6d45dadc26c02daeea8dabee8204",
#     "objectFileHashSha256": "be7241a74fe9a9d30e0631e41533a362b21c8f7aae3e5b6ad319cc15c024ec3f",
#     "objectFilePath": "C:\\Windows\\System32\\tasklist.exe",
#     "objectHashId": "-2212264820798888352",
#     "objectIntegrityLevel": 12288,
#     "objectName": "C:\\Windows\\System32\\tasklist.exe",
#     "objectPid": 18224,
#     "objectSigner": [
#       "Microsoft Windows"
#     ],
#     "objectSignerValid": [
#       true
#     ],
#     "objectTrueType": 7,
#     "objectUser": "UCJ2605VE02",
#     "objectUserDomain": "FARMATODO",
#     "pname": "751",
#     "processCmd": "C:\\Windows\\system32\\cmd.exe /c \"\"C:\\biopagobdv\\autobiopago.bat\" \"",
#     "processFileHashMd5": "8a2122e8162dbef04694b9c3e0b6cdee",
#     "processFileHashSha1": "f1efb0fddc156e4c61c5f78a54700e4e7984d55d",
#     "processFileHashSha256": "b99d61d874728edc0918ca0eb10eab93d381e7367e377406e65963366c874450",
#     "processFilePath": "C:\\Windows\\System32\\cmd.exe",
#     "processHashId": "-8252357020609946928",
#     "processName": "C:\\Windows\\System32\\cmd.exe",
#     "processPid": 12920,
#     "processUser": "UCJ2605VE02",
#     "tags": [
#       "MITRE.T1057",
#       "MITRE.T1059.003",
#       "XSAE.F1796",
#       "MITRE.T1059",
#       "MITRE.T1010"
#     ],
#     "uuid": "5f72476a-2a77-4280-a8e8-c274b3326b82",
#     "productCode": "xes",
#     "filterRiskLevel": "info",
#     "osDescription": "Windows 10 Pro (64 bit) build 19044",
#     "processFileHashId": 4782316872209302322,
#     "processLaunchTime": 1706163419460.0,
#     "processSigner": [
#       "Microsoft Windows"
#     ],
#     "processSignerValid": [
#       true
#     ],
#     "processTrueType": 7,
#     "processUserDomain": "FARMATODO",
#     "osName": "Windows",
#     "pver": "1.2.0.4592",
#     "timezone": "UTC-04:00",
#     "eventSourceType": 1,
#     "authId": "463969",
#     "processFileCreation": "1633527033458",
#     "pplat": 5889,
#     "sessionId": 1,
#     "processFileSize": "289792",
#     "processFileModifiedTime": "1633527033473",
#     "plang": 1,
#     "eventHashId": "-5659588344773481699",
#     "osType": "0x00000030",
#     "userDomain": [
#       "FARMATODO"
#     ],
#     "osVer": "10.0.19044",
#     "endpointMacAddress": [
#       "00:07:32:94:57:40"
#     ],
#     "objectFileSize": "106496",
#     "objectFileModifiedTime": "1575709791678",
#     "objectFileCreation": "1575709791678",
#     "objectFileHashId": "1484284139507252747",
#     "objectRunAsLocalAccount": false,
#     "objectLaunchTime": "1706195524242",
#     "objectSessionId": "1",
#     "objectAuthId": "463969"
#   },
#   "ingestedDateTime": "2024-01-25T15:15:45Z",
#   "entityType": "endpoint",
#   "entityName": "CJ2605VE02(fe80::816d:cdcf:e337:bd6c,172.16.214.22)",
#   "endpoint": {
#     "ips": [
#       "fe80::816d:cdcf:e337:bd6c",
#       "172.16.214.22"
#     ],
#     "agentGuid": "cf9d0cf0-dfd5-4d21-8a0d-2d24e76d8cd0",
#     "endpointName": "CJ2605VE02"
#   }
# }


def parse_OAT(output):
    console.debug("Preparing to parse OAT detections...")
    totalCount = output.get("totalCount")
    count = output.get("count")
    items = output.get("items")
    OATs = []

    if count < totalCount:
        console.warn(
            f"There are more detections than the ones shown. Please, increase the 'top' parameter. (Current: {count}, Total: {totalCount})"
        )

    for i in range(len(items)):
        item = items[i]
        if item.get("source") == "detections":
            data = convert_object(item)
            selected_keys = {
                "source",
                "uuid",
                "detectedDateTime",
                "ingestedDateTime",
                "entityType",
                "entityName",
                "endpointName",
                "ips",
                "filterRiskLevel",
                "endpointHostName",
                "processCmd",
                "objectType",
                "processFilePath",
                "tags",
                "tacticId",
                "ruleName",
                "eventName",
                "eventSubName",
                "parentCmd",
                "parentFilePath",
                "parentFileHashSha256",
                "processFileHashSha256",
                "policyId",
                "processName",
                "processPid",
                "parentPid",
                "processFilePath",
                "processCmd",
            }

            selected_elements, other_elements = process_object(data, selected_keys)
            OATs.append("".join(selected_elements + other_elements))
        else:
            data = convert_object(item)
            selected_keys = {
                "entityName",
                "description",
                "mitreTacticIds",
                "mitreTechniqueIds",
                "endpointName",
                "ips",
                "endpointHostName",
                "osDescription",
                "processHashId",
                "processName",
                "processPid",
                "processUser",
                "processUserDomain",
                "processLaunchTime",
                "processCmd",
                "processFileHashId",
                "processFilePath",
                "processFileHashSha256",
                "objectUser",
                "objectUserDomain",
                "objectSessionId",
                "objectFilePath",
                "objectFileHashSha256",
                "objectFileSize",
                "objectName",
                "objectPid",
                "objectCmd",
                "objectRunAsLocalAccount",
                "tags",
                "highlightedObjects",
            }
            selected_elements, other_elements = process_object(data, selected_keys)
            # OATs.append("".join(selected_elements + other_elements))

    return OATs


def process_object(data, selected_keys):
    selected_elements = []
    other_elements = []

    for item in data:
        for key, value in item.items():
            if key in selected_keys:
                selected_elements.append(f"{key.upper()}: {value}")
            else:
                other_elements.append(f"{key.upper()}: {value}")

    # Ordena las listas alfabéticamente
    selected_elements.sort()
    other_elements.sort()

    return selected_elements, other_elements

def convert_object(data):
    converted_data = []

    # Ordena las claves alfabéticamente, excluyendo "filters"
    for key in sorted(data.keys()):
        if key != "filters":
            if isinstance(data[key], dict):
                # Recurre a objetos anidados (como "detail")
                converted_data.extend(convert_object(data[key]))
            else:
                if key == "msg":
                    if type(data[key]) == str:
                        data[key] = data[key].encode()
                    data[key] = binascii.b2a_base64(data[key])
                
                converted_data.append({f"{key}": str(data[key])})

    # Procesa los "filters" al final, ordenando sus claves también
    if "filters" in data:
        for filter_data in data["filters"]:
            for key in sorted(filter_data.keys()):
                converted_data.append(
                    {f"{key}": str(filter_data[key])}
                )  # Aquí estaba el error

    return converted_data


#     activity = ""

#     # Principales
#     activity += f"source: {str(item.get('source'))}#"
#     activity += f"uuid: {str(item.get('uuid'))}#"
#     activity += f"detectedDateTime: {str(item.get('detectedDateTime'))}#"
#     activity += f"ingestedDateTime: {str(item.get('ingestedDateTime'))}#"
#     activity += f"entityType: {str(item.get('entityType'))}#"
#     activity += f"entityName: {str(item.get('entityName'))}#"

#     detail = item.get("detail")

#     excludeKeys = [
#         "endpointHostName",
#         "objectCmd",
#         "objectFileHashMd5",
#         "objectFileHashSha1",
#         "objectFileHashSha256",
#         "objectFilePath",
#         "objectHashId",
#         "objectName",
#         "objectPid",
#         "objectUser",
#         "objectUserDomain",
#         "processCmd",
#         "processFileHashSha1",
#         "processFilePath",
#         "processName",
#         "processPid",
#         "processUser",
#         "osDescription",
#         "processUserDomain",
#         "osName",
#         "objectFileSize",
#         "objectRunAsLocalAccount",
#     ]

#     for key in excludeKeys:
#         activity += f"{key}: {str(detail.get(f'{key}'))}#"

#     return activity

# def detections_OAT(item):
#     detection = ""

#     # Principales
#     detection += f"source: {str(item.get('source'))}#"
#     detection += f"uuid: {str(item.get('uuid'))}#"
#     detection += f"detectedDateTime: {str(item.get('detectedDateTime'))}#"
#     detection += f"ingestedDateTime: {str(item.get('ingestedDateTime'))}#"
#     detection += f"entityType: {str(item.get('entityType'))}#"
#     detection += f"entityName: {str(item.get('entityName'))}#"

#     detail = item.get("detail")

#     # Detalles
#     excludeKeys = [
#         "objectFileName",
#         "objectFilePath",
#         "objectFileSize",
#         "objectFileHashSha1",
#         "filePath",
#         "fileHash",
#         "objectType",
#         "ruleName",
#         "malName",
#         "eventName",
#         "eventSubName",
#         "fullPath",
#         "eventId",
#         "scanType",
#         "malDst",
#         "domainName",
#         "malType",
#         "firstActResult",
#         "channel",
#         "malFamily",
#     ]

#     for key in excludeKeys:
#         activity += f"{key}: {str(detail.get(f'{key}'))}#"

#     # source: endpointActivityData#uuid: 70a7fcc3-a429-4bd0-9f8e-cdff7677026a#detectedDateTime: 2024-01-25T16:29:01Z#ingestedDateTime: 2024-01-25T16:32:53Z#entityType: endpoint#entityName: CJ2501VE01(fe80::44d6:a52c:d0:b201,172.16.113.21)#endpointHostName: CJ2501VE01#objectCmd: sc  query OracleServiceXSTOREDB #objectFileHashMd5: 3fb5cf71f7e7eb49790cb0e663434d80#objectFileHashSha1: b4979a9f970029889713d756c3f123643dde73da#objectFileHashSha256: 41f067c3a11b02fe39947f9eba68ae5c7cb5bd1872a6009a4cd1506554a9aba9#objectFilePath: C:\Windows\System32\sc.exe#objectHashId: -582481833512562970#objectName: C:\Windows\System32\sc.exe#objectPid: 19676#objectUser: UCJ2501VE01#objectUserDomain: FARMATODO#processCmd: C:\Windows\SYSTEM32\cmd.exe /c ""c:\mantenimiento\check_xstoredbsvc.bat""#processFileHashSha1: f1efb0fddc156e4c61c5f78a54700e4e7984d55d#processFilePath: C:\Windows\System32\cmd.exe#processName: C:\Windows\System32\cmd.exe#processPid: 20024#processUser: UCJ2501VE01#osDescription: Windows 10 Pro (64 bit) build 19044#processUserDomain: FARMATODO#osName: Windows#objectFileSize: 72192#objectRunAsLocalAccount: False#

#     for key, value in detail.items():
#         if key not in excludeKeys:
#             if key == "msg":
#                 if type(value) == str:
#                     value = value.encode()
#                 value = binascii.b2a_base64(value)

#             if isinstance(value, (str, bool, int, list)):
#                 detection += f"{key}: {str(value[0] if isinstance(value, list) and len(value) == 1 else str(value))}#"
#             else:
#                 detection += f"{key}: {str(value)}#"

#     filters = item.get("filters")

#     for x in range(len(filters)):
#         _filter = filters[x]
#         highlightedObjects = _filter.get("highlightedObjects")

#         for obj in highlightedObjects:
#             if isinstance(value, (str, bool, int, list)):
#                 detection += f"{obj.get('field')}: {str(obj.get('value')[0] if isinstance(obj.get('value'), list) and len(obj.get('value')) == 1 else obj.get('value'))}#"
#             else:
#                 detection += f"filter_{obj.get('field')}: {str(obj.get('value'))}#"

#     return detection


# for key, value in detail.items():
#     if (key not in excludeKeys):
#         if key == "msg":
#             if type(value) == str:
#                 value = value.encode()
#             value = binascii.b2a_base64(value)

#         if isinstance(value, (str, bool, int, list)):
#             detection += f"{key}: {str(value[0] if isinstance(value, list) and len(value) == 1 else str(value))}#"
#         else:
#             detection += f"{key}: {str(value)}#"


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
