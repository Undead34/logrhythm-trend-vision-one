import jsonschema

endpointActivityDataSchema = {
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
                                "value": {
                                    "anyOf": [{"type": "string"}, {"type": "number"}]
                                },
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
                "endpointGuid": {"type": "string"},
                "endpointHostName": {"type": "string"},
                "endpointIp": {"type": "array", "items": {"type": "string"}},
                "eventId": {"type": "string"},
                "eventSubId": {"type": "integer"},
                "eventTime": {"type": "string"},
                "firstSeen": {"type": "string"},
                "lastSeen": {"type": "string"},
                "logonUser": {"type": "array", "items": {"type": "string"}},
                "objectCmd": {"type": "string"},
                "objectFileHashMd5": {"type": "string"},
                "objectFileHashSha1": {"type": "string"},
                "objectFileHashSha256": {"type": "string"},
                "objectFilePath": {"type": "string"},
                "objectHashId": {"type": "string"},
                "objectName": {"type": "string"},
                "objectPid": {"type": "integer"},
                "objectUser": {"type": "string"},
                "pname": {"type": "string"},
                "processCmd": {"type": "string"},
                "processFileHashMd5": {"type": "string"},
                "processFileHashSha1": {"type": "string"},
                "processFileHashSha256": {"type": "string"},
                "processFilePath": {"type": "string"},
                "processHashId": {"type": "string"},
                "processName": {"type": "string"},
                "processPid": {"type": "integer"},
                "processUser": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "uuid": {"type": "string"},
                "productCode": {"type": "string"},
                "filterRiskLevel": {"type": "string"},
                "osDescription": {"type": "string"},
                "processFileHashId": {"type": "integer"},
                "processLaunchTime": {"type": "number"},
                "endpointMacAddress": {"type": "array", "items": {"type": "string"}},
                "eventSourceType": {"type": "integer"},
                "timezone": {"type": "string"},
                "pplat": {"type": "integer"},
                "objectLaunchTime": {"type": "string"},
                "objectFileHashId": {"type": "string"},
                "objectRunAsLocalAccount": {"type": "boolean"},
                "osType": {"type": "string"},
                "osName": {"type": "string"},
                "osVer": {"type": "string"},
                "eventHashId": {"type": "string"},
                "plang": {"type": "integer"},
                "userDomain": {"type": "array", "items": {"type": "string"}},
                "pver": {"type": "string"},
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


class EndpointActivityData:
    def __init__(self) -> None:
        self.validator = jsonschema.Draft7Validator(endpointActivityDataSchema)
        self.validator.check_schema(endpointActivityDataSchema)

    def isValid(self, data: dict) -> bool:
        try:
            self.validator.validate(data)
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False
        except Exception as e:
            print(e)
            return False

    # object is a valid endpointActivityDataSchema
    # This function returns a string un KEY: VALUE format with all relevant information of detection_shema considering the security in the mind
    def parser(self, object: dict):
        detection = ""
        detection += "Source: " + str(object.get("source")) + "\n"
        detection += "UUID: " + str(object.get("uuid")) + "\n"
        detection += "Detected Date Time: " + str(object.get("detectedDateTime")) + "\n"
        detection += "Ingested Date Time: " + str(object.get("ingestedDateTime")) + "\n"
        detection += "Entity Type: " + str(object.get("entityType")) + "\n"
        detection += "Entity Name: " + str(object.get("entityName")) + "\n"
        
        object_details = object["detail"]
        details = ""
        details += "Endpoint GUID: " + str(object_details.get("endpointGuid")) + "\n"
        details += "Endpoint Host Name: " + str(object_details.get("endpointHostName")) + "\n"
        details += "Endpoint IP: " + str(object_details.get("endpointIp")) + "\n"
        details += "Event ID: " + str(object_details.get("eventId")) + "\n"
        details += "Event Sub ID: " + str(object_details.get("eventSubId")) + "\n"
        details += "Event Time: " + str(object_details.get("eventTime")) + "\n"
        details += "First Seen: " + str(object_details.get("firstSeen")) + "\n"
        details += "Last Seen: " + str(object_details.get("lastSeen")) + "\n"
        details += "Logon User: " + str(object_details.get("logonUser")) + "\n"
        details += "Object Cmd: " + str(object_details.get("objectCmd")) + "\n"
        details += "Object File Hash Md5: " + str(object_details.get("objectFileHashMd5")) + "\n"
        details += "Object File Hash Sha1: " + str(object_details.get("objectFileHashSha1")) + "\n"
        details += "Object File Hash Sha256: " + str(object_details.get("objectFileHashSha256")) + "\n"
        details += "Object File Path: " + str(object_details.get("objectFilePath")) + "\n"
        details += "Object Hash ID: " + str(object_details.get("objectHashId")) + "\n"
        details += "Object Name: " + str(object_details.get("objectName")) + "\n"
        details += "Object PID: " + str(object_details.get("objectPid")) + "\n"
        details += "Object User: " + str(object_details.get("objectUser")) + "\n"
        details += "Process Name: " + str(object_details.get("pname")) + "\n"
        details += "Process Cmd: " + str(object_details.get("processCmd")) + "\n"
        details += "Process File Hash Md5: " + str(object_details.get("processFileHashMd5")) + "\n"
        details += "Process File Hash Sha1: " + str(object_details.get("processFileHashSha1")) + "\n"
        details += "Process File Hash Sha256: " + str(object_details.get("processFileHashSha256")) + "\n"
        details += "Process File Path: " + str(object_details.get("processFilePath")) + "\n"
        details += "Process Hash ID: " + str(object_details.get("processHashId")) + "\n"
        details += "Process Name: " + str(object_details.get("processName")) + "\n"
        details += "Process PID: " + str(object_details.get("processPid")) + "\n"
        details += "Process User: " + str(object_details.get("processUser")) + "\n"
        details += "Tags: " + str(object_details.get("tags")) + "\n"
        details += "Details UUID: " + str(object_details.get("uuid")) + "\n"
        details += "Product Code: " + str(object_details.get("productCode")) + "\n"
        details += "Filter Risk Level: " + str(object_details.get("filterRiskLevel")) + "\n"
        details += "OS Description: " + str(object_details.get("osDescription")) + "\n"
        details += "Process File Hash ID: " + str(object_details.get("processFileHashId")) + "\n"
        details += "Process Launch Time: " + str(object_details.get("processLaunchTime")) + "\n"
        details += "Endpoint MAC Address: " + str(object_details.get("endpointMacAddress")) + "\n"
        details += "Event Source Type: " + str(object_details.get("eventSourceType")) + "\n"
        details += "Timezone: " + str(object_details.get("timezone")) + "\n"
        details += "Pplat: " + str(object_details.get("pplat")) + "\n"
        details += "Object Launch Time: " + str(object_details.get("objectLaunchTime")) + "\n"
        details += "Object File Hash ID: " + str(object_details.get("objectFileHashId")) + "\n"
        details += "Object Run As Local Account: " + str(object_details.get("objectRunAsLocalAccount")) + "\n"
        details += "OS Type: " + str(object_details.get("osType")) + "\n"
        details += "OS Name: " + str(object_details.get("osName")) + "\n"
        details += "OS Ver: " + str(object_details.get("osVer")) + "\n"
        details += "Event Hash ID: " + str(object_details.get("eventHashId")) + "\n"
        details += "Plang: " + str(object_details.get("plang")) + "\n"
        details += "User Domain: " + str(object_details.get("userDomain")) + "\n"
        details += "Pver: " + str(object_details.get("pver")) + "\n"
        
        detection += details

        object_endpoint = object["endpoint"]
        endpoint = ""
        endpoint += "IPS: " + str(object_endpoint.get("ips")) + "\n"
        endpoint += "Agent GUID: " + str(object_endpoint.get("agentGuid")) + "\n"
        endpoint += "Endpoint Name: " + str(object_endpoint.get("endpointName")) + "\n"
        detection += endpoint

        filters = ""
        
        for filter in object["filters"]:
            filters += "ID: " + str(filter.get("id")) + "\n"
            filters += "Name: " + str(filter.get("name")) + "\n"
            filters += "Description: " + str(filter.get("description")) + "\n"
            filters += "Highlighted Objects: " + str(filter.get("highlightedObjects")) + "\n"
            filters += "Mitre Tactic IDs: " + str(filter.get("mitreTacticIds")) + "\n"
            filters += "Mitre Technique IDs: " + str(filter.get("mitreTechniqueIds")) + "\n"
            filters += "Risk Level: " + str(filter.get("riskLevel")) + "\n"
            filters += "Type: " + str(filter.get("type")) + "\n"
            detection += filters
        
        return detection