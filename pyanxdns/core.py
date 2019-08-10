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
    DELETE = "delete"

    def __str__(self):
        return self.value


class Client:
    def __init__(self, domain, apikey):
        self.domain = domain
        self.apikey = apikey

    def _communicate(self, method=Method.GET, headers={}, data_json=None, query_string=""):
        if not 'apikey' in headers:
            headers["apikey"] = self.apikey
        
        if not 'Content-Type' in headers:
            headers["Content-Type"] = "application/json"
        
        api_url = api_url_base + query_string

        response = None

        try:
            response = requests.request(str(method), api_url, headers=headers, json=data_json, allow_redirects=True)
        except Exception as e:
            raise APIError(str(e))

        if response is None:
            raise APIError("Did not get a response from API")

        logger.debug(response.content)
        
        if response.status_code in [200, 201]:
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
        response = self._communicate(query_string='?domain={}'.format(self.domain))
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
    
    def parse_by_line(self, all_records, line):
        for record in all_records:
            if record['line'] == line:
                return record

        return None

    def parse_by_txt(self, all_records, txt, name=None):
        if name is not None:
            return [x for x in all_records if x['txtdata'] == txt and x['type'] == 'TXT' and x['name'] == 'name']
        else:
            return [x for x in all_records if x['txtdata'] == txt and x['type'] == 'TXT']

    def get_by_name(self, name):
        all_records = self.get_all()
        
        return self.parse_by_name(all_records, name)

    def get_by_line(self, line):
        all_records = self.get_all()
        
        return self.parse_by_line(all_records, line)
    
    def get_by_txt(self, txt, name=None):
        if name is not None:
            records = self.get_by_name(name)
        else:
            records = self.get_all()
        
        return self.parse_by_txt(records, txt)

    def _create_json_data(self, type, name, address=None, ttl=3600, txtdata=None, line=None):
        data = {
            "domain": self.domain,
            "type": str(type),
            "name": name,
            "ttl": ttl
        }   

        if address is not None:
            data["address"] = address

        if txtdata is not None:
             data["txtdata"] = txtdata

        if line is not None:
            data["line"] = str(line)

        return data


    def add_txt_record(self, name, txtdata, ttl=3600):
        data = self._create_json_data(RecordType.TEXT, name, address="", ttl=ttl, txtdata=txtdata)

        self._communicate(method=Method.POST, data_json=data)

    def add_a_record(self, name, address, ttl=3600):
        data = self._create_json_data(RecordType.A, name, address=address, ttl=ttl)

        self._communicate(method=Method.POST, data_json=data)
    
    def add_cname_record(self, name, address, ttl=3600):
        data = self._create_json_data(RecordType.CNAME, name, address=address, ttl=ttl)

        self._communicate(method=Method.POST, data_json=data)

    def verify_or_get_record(self, line, name, type=None):
        if line is not None:
            record = self.get_by_line(line)
            if record is None:
                raise APIError("0 records with provided line number.")
        elif name is not None:
            records = self.get_by_name(name)
            if len(records) == 0:
                raise APIError("0 records with that name.")
            elif len(records) > 1:
                raise APIError(">1 record with that name. Specify line instead of name.")
            record = records[0]
        else:
            raise APIError("Line or name needs to be provided")

        if record is None:
            raise APIError("No record found")

        if type is not None and record["type"] != str(type):
            raise APIError("Record is not a {}.".format(type))

        return record
    
    def update_txt_record(self, txt, name=None, ttl=3600, line=None, find_txt=None):
        # Find line
        if line is None and find_txt is not None:
            records = self.get_by_txt(find_txt, name=name)
            if len(records) == 0:
                raise APIError("0 records with that name.")
            elif len(records) > 1:
                raise APIError(">1 record with that name. Specify line instead of name.")
            record = records[0]
        else:
            record = self.verify_or_get_record(line, name, RecordType.TEXT)
        
        if record is None:
            raise APIError("No record found")

        data = self._create_json_data(RecordType.TEXT, record["name"], txtdata=txt, ttl=ttl, line=record["line"])

        self._communicate(method=Method.PUT, data_json=data)
    
    def update_a_record(self, address, name=None, ttl=3600, line=None):
        # Find line
        record = self.verify_or_get_record(line, name, RecordType.A)

        data = self._create_json_data(RecordType.A, name=record["name"], address=address, ttl=ttl, line=record["line"])

        self._communicate(method=Method.PUT, data_json=data)
    
    def update_cname_record(self, address, name=None, ttl=3600, line=None):
        # Find line
        record = self.verify_or_get_record(line, name, RecordType.CNAME)
        
        data = self._create_json_data(RecordType.CNAME, name=record["name"], address=address, ttl=ttl, line=record["line"])

        self._communicate(method=Method.PUT, data_json=data)

    def delete_line(self, line):
        # Find line
        record = self.verify_or_get_record(line, None)

        data = self._create_json_data(RecordType.CNAME, name=record["name"], line=record["line"])
        del(data["name"])
        del(data["type"])
        del(data["ttl"])
        
        self._communicate(Method.DELETE, data_json=data)
    
    def delete_by_txt(self, txt, name=None):
        # Find line
        records = self.get_by_txt(txt, name=name)

        if len(records) == 0:
            raise APIError("0 records with that name.")
        elif len(records) > 1:
            raise APIError(">1 record with that name. Specify line instead of name.")
        
        record = records[0]

        data = self._create_json_data(RecordType.CNAME, name=record["name"], line=record["line"])
        del(data["name"])
        del(data["type"])
        del(data["ttl"])
        self._communicate(Method.DELETE, data_json=data)
    
    def delete_by_name(self, name):
        # Find line
        record = self.verify_or_get_record(None, name)

        data = self._create_json_data(RecordType.CNAME, name=record["name"], line=record["line"])
        del(data["name"])
        del(data["type"])
        del(data["ttl"])
        
        self._communicate(Method.DELETE, data_json=data)

if __name__ == "__main__":
    pass
