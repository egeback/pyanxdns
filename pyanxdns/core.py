import json
import requests
import logging

from enum import Enum
from .helpers import format_json


logger = logging.getLogger(__name__)
api_url_base = "https://dyn.anx.se/api/dns/"


class APIError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class RecordType(Enum):
    TEXT = "TXT"
    A = "A"
    CNAME = "CNAME"

    def __str__(self):
        return self.value


class Method(Enum):
    GET = "get"
    PUT = "put"
    POST = "post"

    def __str__(self):
        return self.value
    


class API:
    def __init__(self, domain, apikey):
        self.domain = domain
        self.apikey = apikey

    def _communicate(self, body=None, method=Method.GET, headers={}, data=None):
        if not 'apikey' in headers:
            headers["apikey"] = self.apikey
        
        if not 'Content-Type' in headers:
            headers["Content-Type"] = "application/json"
        
        api_url = api_url_base +  '?domain={}'.format(self.domain)

        response = None

        response = requests.request(str(method), api_url, headers=headers, json=data, allow_redirects=True)

        if response is None:
            raise APIError("Did not get a response from API")

        logger.debug(response.content)
        
        if response.status_code == 200:
            return (json.loads(response.content))
        else:
            logger.error('[!] HTTP {0} calling [{1}]:{2}'.format(response.status_code, api_url, response.content))
            try:
                j = json.loads(response.content)
                raise APIError(j['status'])
            except (ValueError):
                pass 
            raise APIError(response.content)

    def get_all(self):
        response = self._communicate(self)
        return response['dnsRecords']

    def parse_by_name(self, all_records, name):
        n = name
        if not n.endswith('.'):
            n = n + '.'

        records = []
        for record in all_records:
            if record['name'] == n:
                records.append(record)
        
        return records

    def get_by_name(self, name):
        all_records = self.get_all()
        
        return self.parse_by_name(all_records, name)

    def _create_json_data(self, name, adress="", type=RecordType.TEXT, ttl=3600, txtdata=None, line=None):
        data = {
            "domain": self.domain,
            "name": name,
            "address": adress,
            "type": type,
            "ttl": ttl
        }

        if txtdata is not None:
             data["txtdata"] = txtdata

        if line is not None:
            data["line"] = str(line)

        return json.dumps(data)


    def add_txt_record(self, name, txtdata, ttl=3600):
        data = self._create_json_data(name, ttl=ttl, txtdata=txtdata)


    
    def add_a_record(self, name, address, ttl=3600):
        pass
    
    def add_cname(self, name, cname, ttl=3600):
        pass
    
    def update_txt_record(self, name, ttl=3600):
        pass
    
    def update_a_record(self, name, address, ttl=3600):
        pass
    
    def update_cname(self, name, cname, ttl=3600):
        pass

    def delete_row(self, row):
        pass
    
    def delete_by_name(self, name):
        pass

if __name__ == "__main__":
    pass
