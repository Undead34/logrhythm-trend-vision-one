import jsonschema

detections_schema = {
    "type": "object",
    "properties": {
        "source": {"type": "string"},
        "uuid": {"type": "string"},
        "detectedDateTime": {"type": "string"},
        "ingestedDateTime": {"type": "string"},
        "entityType": {"type": "string"},
        "entityName": {"type": "string"},
        "filters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "highlightedObjects": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {"type": "string"},
                                "type": {"type": "string"},
                                "value": {"type": "string"},
                            },
                        },
                    },
                    "mitreTacticIds": {"type": "array", "items": {"type": "string"}},
                    "mitreTechniqueIds": {"type": "array", "items": {"type": "string"}},
                    "riskLevel": {"type": "string"},
                    "type": {"type": "string"},
                },
            },
        },
        "detail": {
            "type": "object",
            "properties": {
                "uuid": {"type": "string"},
                "filterRiskLevel": {"type": "string"},
                "endpointHostName": {"type": "string"},
                "endpointGUID": {"type": "string"},
                "objectFilePath": {"type": "string"},
                "objectFileHashSha1": {"type": "string"},
                "objectFileHashSha256": {"type": "string"},
                "objectFileHashMd5": {"type": "string"},
                "processCmd": {"type": "string"},
                "objectType": {"type": "string"},
                "processFilePath": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "tacticId": {"type": "array", "items": {"type": "string"}},
                "ruleName": {"type": "string"},
                "eventName": {"type": "string"},
                "eventSubName": {"type": "string"},
                "parentCmd": {"type": "string"},
                "parentFilePath": {"type": "string"},
                "parentFileHashSha1": {"type": "string"},
                "parentFileHashSha256": {"type": "string"},
                "parentFileHashMd5": {"type": "string"},
                "processFileHashSha1": {"type": "string"},
                "processFileHashSha256": {"type": "string"},
                "processFileHashMd5": {"type": "string"},
                "eventId": {"type": "string"},
                "policyId": {"type": "string"},
                "productCode": {"type": "string"},
                "pname": {"type": "string"},
                "act": {"type": "array", "items": {"type": "string"}},
                "deviceGUID": {"type": "string"},
                "instanceId": {"type": "string"},
                "processName": {"type": "string"},
                "processPid": {"type": "integer"},
                "parentPid": {"type": "integer"},
                "eventTime": {"type": "string"},
                "eventSourceType": {"type": "integer"},
                "rt_utc": {"type": "string"},
                "rt": {"type": "string"},
                "behaviorCat": {"type": "string"},
                "engineOperation": {"type": "string"},
                "engVer": {"type": "string"},
                "mpname": {"type": "string"},
                "mpver": {"type": "string"},
                "patVer": {"type": "string"},
                "processSigner": {"type": "array", "items": {"type": "string"}},
                "riskLevel": {"type": "string"},
                "parentName": {"type": "string"},
                "parentSigner": {"type": "array", "items": {"type": "string"}},
                "parentSignerValid": {"type": "array", "items": {"type": "boolean"}},
                "processSignerValid": {"type": "array", "items": {"type": "boolean"}},
                "logKey": {"type": "string"},
                "processHashId": {"type": "string"},
                "parentHashId": {"type": "string"},
                "objectFileSize": {"type": "string"},
            },
        },
        "endpoint": {
            "type": "object",
            "properties": {
                "ips": {"type": "array", "items": {"type": "string"}},
                "agentGuid": {"type": "string"},
                "endpointName": {"type": "string"},
            },
        },
    },
}

class DetectionsSchema:
    def __init__(self) -> None:
        self.validator = jsonschema.Draft7Validator(detections_schema)
        self.validator.check_schema(detections_schema)

    def isValid(self, data: dict) -> bool:
        try:
            self.validator.validate(data)
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False
        except Exception as e:
            print(e)
            return False

    # object is a valid detection_schema
    # This function returns a string un KEY: VALUE format with all relevant information of detection_shema considering the security in the mind
    def parser(self, object: dict):
        try:
            detections = ""
            detections += "Source: " + object.get("source") + "\n"
            detections += "UUID: " + object.get("uuid") + "\n"
            detections += "Detected Date Time: " + object.get("detectedDateTime") + "\n"
            detections += "Ingested Date Time: " + object.get("ingestedDateTime") + "\n"
            detections += "Entity Type: " + object.get("entityType") + "\n"
            detections += "Entity Name: " + object.get("entityName") + "\n"

            object_details: dict = object.get("detail")

            details = ""
            details += "UUID: " + str(object_details.get("uuid")) + "\n"
            details += "Filter Risk Level: " + str(object_details.get("filterRiskLevel")) + "\n"
            details += "Endpoint Host Name: " + str(object_details.get("endpointHostName")) + "\n"
            details += "Endpoint GUID: " + str(object_details.get("endpointGUID")) + "\n"
            details += "Object File Path: " + str(object_details.get("objectFilePath")) + "\n"
            details += "Object File Hash Sha1: " + str(object_details.get("objectFileHashSha1")) + "\n"
            details += "Object File Hash Sha256: " + str(object_details.get("objectFileHashSha256")) + "\n"
            details += "Object File Hash Md5: " + str(object_details.get("objectFileHashMd5")) + "\n"
            details += "Process Cmd: " + str(object_details.get("processCmd")) + "\n"
            details += "Object Type: " + str(object_details.get("objectType")) + "\n"
            details += "Process File Path: " + str(object_details.get("processFilePath")) + "\n"
            details += "Tags: " + str(object_details.get("tags")) + "\n"
            details += "Tactic Id: " + str(object_details.get("tacticId")) + "\n"
            details += "Rule Name: " + str(object_details.get("ruleName")) + "\n"
            details += "Event Name: " + str(object_details.get("eventName")) + "\n"
            details += "Event Sub Name: " + str(object_details.get("eventSubName")) + "\n"
            details += "Parent Cmd: " + str(object_details.get("parentCmd")) + "\n"
            details += "Parent File Path: " + str(object_details.get("parentFilePath")) + "\n"
            details += "Parent File Hash Sha1: " + str(object_details.get("parentFileHashSha1")) + "\n"
            details += "Parent File Hash Sha256: " + str(object_details.get("parentFileHashSha256")) + "\n"
            details += "Parent File Hash Md5: " + str(object_details.get("parentFileHashMd5")) + "\n"
            details += "Process File Hash Sha1: " + str(object_details.get("processFileHashSha1")) + "\n"
            details += "Process File Hash Sha256: " + str(object_details.get("processFileHashSha256")) + "\n"
            details += "Process File Hash Md5: " + str(object_details.get("processFileHashMd5")) + "\n"
            details += "Event Id: " + str(object_details.get("eventId")) + "\n"
            details += "Policy Id: " + str(object_details.get("policyId")) + "\n"
            details += "Product Code: " + str(object_details.get("productCode")) + "\n"
            details += "Pname: " + str(object_details.get("pname")) + "\n"
            details += "Act: " + str(object_details.get("act")) + "\n"
            details += "Device GUID: " + str(object_details.get("deviceGUID")) + "\n"
            details += "Instance Id: " + str(object_details.get("instanceId")) + "\n"
            details += "Process Name: " + str(object_details.get("processName")) + "\n"
            details += "Process Pid: " + str(object_details.get("processPid")) + "\n"
            details += "Parent Pid: " + str(object_details.get("parentPid")) + "\n"
            details += "Event Time: " + str(object_details.get("eventTime")) + "\n"
            details += "Event Source Type: " + str(object_details.get("eventSourceType")) + "\n"
            details += "Rt Utc: " + str(object_details.get("rt_utc")) + "\n"
            details += "Rt: " + str(object_details.get("rt")) + "\n"
            details += "Behavior Cat: " + str(object_details.get("behaviorCat")) + "\n"
            details += "Engine Operation: " + str(object_details.get("engineOperation")) + "\n"
            details += "Eng Ver: " + str(object_details.get("engVer")) + "\n"
            details += "Mpname: " + str(object_details.get("mpname")) + "\n"
            details += "Mpver: " + str(object_details.get("mpver")) + "\n"
            details += "Pat Ver: " + str(object_details.get("patVer")) + "\n"
            details += "Process Signer: " + str(object_details.get("processSigner")) + "\n"
            details += "Risk Level: " + str(object_details.get("riskLevel")) + "\n"
            details += "Parent Name: " + str(object_details.get("parentName")) + "\n"
            details += "Parent Signer: " + str(object_details.get("parentSigner")) + "\n"
            details += "Parent Signer Valid: " + str(object_details.get("parentSignerValid")) + "\n"
            details += "Process Signer Valid: " + str(object_details.get("processSignerValid")) + "\n"
            details += "Log Key: " + str(object_details.get("logKey")) + "\n"
            details += "Process Hash Id: " + str(object_details.get("processHashId")) + "\n"
            details += "Parent Hash Id: " + str(object_details.get("parentHashId")) + "\n"
            details += "Object File Size: " + str(object_details.get("objectFileSize")) + "\n"

            detections += details

            endpoint = object.get("endpoint")
            endpoints = ""
            endpoints += "IPS: " + str(endpoint.get("ips")) + "\n"
            endpoints += "Agent GUID: " + str(endpoint.get("agentGuid")) + "\n"
            endpoints += "Endpoint Name: " + str(endpoint.get("endpointName")) + "\n"
            detections += endpoints

            filters = object.get("filters")
            filter = ""
            
            for x in range(len(filters)):
                filter += "ID: " + str(filters[x].get("id")) + "\n"
                filter += "Name: " + str(filters[x].get("name")) + "\n"
                filter += "Description: " + str(filters[x].get("description")) + "\n"
                highlightedObjects = filters[x].get("highlightedObjects")
                highlightedObject = ""
                for y in range(len(highlightedObjects)):
                    highlightedObject += "Field: " + str(highlightedObjects[y].get("field")) + "\n"
                    highlightedObject += "Type: " + str(highlightedObjects[y].get("type")) + "\n"
                    highlightedObject += "Value: " + str(highlightedObjects[y].get("value")) + "\n"
                filter += "Highlighted Objects: " + highlightedObject
                filter += "Mitre Tactic Ids: " + str(filters[x].get("mitreTacticIds")) + "\n"
                filter += "Mitre Technique Ids: " + str(filters[x].get("mitreTechniqueIds")) + "\n"
                filter += "Risk Level: " + str(filters[x].get("riskLevel")) + "\n"
                filter += "Type: " + str(filters[x].get("type")) + "\n"
                detections += filter

            return detections
        except Exception as e:
            print(e)
            return str(object)