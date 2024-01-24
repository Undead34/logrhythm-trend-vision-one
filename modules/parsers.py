from .schemes.endpointActivityData import EndpointActivityData
from .schemes.detections import DetectionsSchema
from .loggers import console

def parse_OAT(output):
    console.debug("Preparing to parse OAT detections...")
    print(output)

    # totalCount = output.get("totalCount")
    # count = output.get("count")
    # items = output.get("items")

    # if count < totalCount:
    #     console.warn(f"There are more detections than the ones shown. Please, increase the 'top' parameter. (Current: {count}, Total: {totalCount})")

    # for i in range(len(items)):
        # item = items[i]
        # print(item)
        # console.debug(f"Item {i}: {item.get('source')}")   

    OATs = []
    return OATs



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