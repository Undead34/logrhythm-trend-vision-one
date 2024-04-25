import requests
import binascii
import time
import os

from utils import get_region, dict_to_key_value, order_dict_by_relevance, valid_unicode
from utils.dateutils import startDateTime, endDateTime


class API():
    url_base: str
    headers: dict

    def __init__(self, mode: str = "normal") -> None:
        self.url_base = "https://" + get_region(os.environ.get("REGION"))
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("API_TOKEN")
        }

    def _get_workbench_data(self):
        url_path = "/v3.0/workbench/alerts"
        url = self.url_base + url_path

        query_params = {
            'startDateTime': startDateTime(),
            'endDateTime': endDateTime(),
            'dateTimeTarget': 'createdDateTime',
            'orderBy': 'createdDateTime desc'
        }

        data = self.get_items(url, query_params)
        items = data.get("items")
        result = []

        for x in range(len(items)):
            result.append(parse_workbench(items[x]))

        return result

    def _get_OAT_data(self):
        url_path = "/v3.0/oat/detections"
        url = self.url_base + url_path

        query_params = {
            'detectedStartDateTime': startDateTime(),
            'detectedEndDateTime': endDateTime(),
            # 'ingestedStartDateTime': startDateTime(60),
            # 'ingestedEndDateTime': endDateTime(),
            'top': '200'
        }

        headers = {
            # (riskLevel eq 'low') or
            'TMV1-Filter': "(riskLevel eq 'medium') or (riskLevel eq 'high') or (riskLevel eq 'critical')"
        }

        data = self.get_items(url, query_params, headers)
        items = data.get("items")
        result = []

        for x in range(len(items)):
            result.append(parse_OAT(items[x]))

        return result

    def _get_audit_logs_data(self):
        url_path = "/v3.0/audit/logs"
        url = self.url_base + url_path

        query_params = {
            'startDateTime': startDateTime(),
            'endDateTime': endDateTime(),
            'orderBy': 'loggedDateTime desc',
            'top': '200',
            'labels': 'matched'
        }

        headers = {
            # Ir modificando dependiendo de los logs
            'TMV1-Filter': "(category eq 'Account Management') and (activity eq 'Add user account')"
        }

        data = self.get_items(url, query_params)
        items = data.get("items")
        result = []

        for x in range(len(items)):
            result.append(parse_audit_logs(items[x]))

        return result

    def _get_detections_data(self):
        url_path = "/v3.0/search/detections"
        url = self.url_base + url_path

        query_params = {
            'startDateTime': startDateTime(),
            'endDateTime': endDateTime(),
            'top': '500',
            'select': 'empty',
            'mode': 'default'
        }

        headers = {
            'TMV1-Query': 'YOUR_QUERY (string)'
        }

    def collect_data(self):
        workbench_data = self._get_workbench_data()
        audit_OAT_data = self._get_OAT_data()
        audit_logs_data = self._get_audit_logs_data()
        # self._get_detections_data()

        return {
            "workbench": workbench_data,
            "OAT": audit_OAT_data,
            "audit_logs": audit_logs_data,
            "detections": [],
        }

    def get_items(self, url, query_params, headers={}):
        items = []
        results = {}

        next_link = None

        while True:
            if next_link is None:
                r = self.fetch(url, query_params, headers)
            else:
                r = self.fetch(next_link, headers=headers)

            if r and isinstance(r, (dict, str)):
                if "items" in r:
                    items.extend(r["items"])

                if not "nextLink" in r:
                    results = r
                    r["items"] = items
                    break

                next_link = r.get("nextLink")
            else:
                break

        return results

    def fetch(self, url, query_params={}, headers={}, retries=3):
        for i in range(retries):
            try:
                header = self.headers.copy()
                header.update(headers)

                r = requests.get(url, params=query_params, headers=header)

                if r.status_code == 200:
                    if 'application/json' in r.headers.get('Content-Type', '') and len(r.content):
                        return r.json()
                    else:
                        return r.text
                else:
                    print(r.status_code, r.text, url)
                    return None

            except Exception as e:
                print(type(e))
                print(e)

                if i < retries - 1:  # i is zero indexed
                    print("Sleeping for 60 seconds")
                    time.sleep(60)  # exponential backoff
                    continue
                else:
                    return None


def parse_workbench(d):
    flattened_dict = dict_to_key_value(d)
    whitelist = "ID STATUS SEVERITY CREATEDDATETIME UPDATEDDATETIME INCIDENTID DESCRIPTION INDICATORS_EXTRA_INFO_0_VALUE INDICATORS_EXTRA_INFO_2_VALUE INDICATORS_EXTRA_INFO_1_TYPE INDICATORS_EXTRA_INFO_1_VALUE IMPACTSCOPE_ENTITIES_EXTRA_INFO_1_ENTITYVALUE_NAME IMPACTSCOPE_ENTITIES_EXTRA_INFO_2_ENTITYVALUE_NAME IMPACTSCOPE_ENTITIES_EXTRA_INFO_1_ENTITYVALUE_IPS_EXTRA_INFO_0 IMPACTSCOPE_ENTITIES_EXTRA_INFO_2_ENTITYTYPE MATCHEDRULES_EXTRA_INFO_0_MATCHEDFILTERS_EXTRA_INFO_0_NAME MATCHEDRULES_EXTRA_INFO_0_MATCHEDFILTERS_EXTRA_INFO_0_MATCHEDDATETIME IMPACTSCOPE_ENTITIES_EXTRA_INFO_0_ENTITYID"
    ordered_dict = order_dict_by_relevance(flattened_dict, whitelist)

    s = '\n'.join(f'{k} = {v}' for k, v in ordered_dict.items())

    s = s.replace('\n', ' ')  # Elimina los saltos de línea
    s = s.replace('\r', ' ')
    s = s.replace('\t', '')  # Elimina las tabulaciones

    return s


def parse_OAT(d):
    flattened_dict = dict_to_key_value(d)
    whitelist = "SOURCE ENTITYNAME ENDPOINT_ENDPOINTNAME INGESTEDDATETIME DETAIL_OSNAME DETAIL_TAGS_EXTRA_INFO_0 DETAIL_OBJECTNAME DETAIL_PARENTCMD FILTERS_EXTRA_INFO_0_DESCRIPTION FILTERS_EXTRA_INFO_0_NAME FILTERS_EXTRA_INFO_0_RISKLEVEL DETAIL_ENDPOINTIP_EXTRA_INFO_0 DETAIL_ENDPOINTHOSTNAME DETAIL_PROCESSCMD DETAIL_PROCESSNAME ENDPOINT_IPS_EXTRA_INFO_0 DETAIL_OSVER DETAIL_PARENTNAME DETAIL_PARENTUSER DETAIL_OSDESCRIPTION DETAIL_FILTERRISKLEVEL DETAIL_TAGS_EXTRA_INFO_1 DETAIL_PROCESSUSER"
    ordered_dict = order_dict_by_relevance(flattened_dict, whitelist)

    s = ''

    for k, v in ordered_dict.items():
        b: bytes = str(v).encode()

        if not b.isascii():
            v = binascii.b2a_base64(b).decode()

        s += f'{k} = {v}\n'

    s = s.replace('\n', ' ')  # Elimina los saltos de línea
    s = s.replace('\r', ' ')
    s = s.replace('\t', '')   # Elimina las tabulaciones

    return s


def parse_audit_logs(d):
    flattened_dict = dict_to_key_value(d)

    s = ''

    for k, v in flattened_dict.items():
        if isinstance(v, (str, bytes)) and not valid_unicode(v):
            v = binascii.b2a_base64(v).decode()

        s += f'{k} = {v}\n'

    s = s.replace('\n', ' ')  # Elimina los saltos de línea
    s = s.replace('\r', ' ')
    s = s.replace('\t', '')  # Elimina las tabulaciones

    return s
