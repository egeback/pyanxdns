import argparse
import os
from .core import API
from .core import api_url_base
from .helpers import format_json


def add_base_arguments(parser, key, domain):
    parser.add_argument("-k", "--apikey", required=False, help="API key used in request header", default=key)
    parser.add_argument("-d", "--domain", required=False, help="Domain name", default=domain)
    parser.add_argument("-v", "--verbose", required=False, help="Verbose", default=False, action='store_true')
    parser.add_argument('-n', '--name', required=False, help='Name parameter', default=None)

def add_extended_arguments(parser, key, domain):
    parser.add_argument('-t', '--ttl', required=False, help='Time to live parameter', default=None)
    parser.add_argument('-x', '--text', required=False, help='Txt parameter', default=None)

class CLI:
    def start(self, *param):
        parser = argparse.ArgumentParser()
        key = os.environ['ANXDNS_APIKEY'] if 'ANXDNS_APIKEY' in os.environ else None
        domain = os.environ['ANXDNS_DOMAIN'] if 'ANXDNS_DOMAIN' in os.environ else None
        
        subparsers = parser.add_subparsers(title='Actions', help='Action to perform', dest="action")
        parser_get = subparsers.add_parser('get', help='Get records', aliases=['g'])
        
        parser_add = subparsers.add_parser('add', help='Add record', aliases=['a'])
        
        parser_update = subparsers.add_parser('update', help='Update record', aliases=['u'])
        parser_update.add_argument('-l', '--line', required=False, help='line parameter', default=None)

        parser_delete = subparsers.add_parser('delete', help='Delete record', aliases=['d', 'del'])
        parser_delete.add_argument('-l', '--line', required=False, help='line parameter', default=None)

        for p in [parser, parser_add, parser_get, parser_update, parser_delete]:
            add_base_arguments(p, key, domain)
            if p is not parser_get:
                add_extended_arguments(p, key, domain)

        args = parser.parse_args()

        api_key = args.apikey
        domain = args.domain
        verbose = args.verbose
        method = args.action

        api = API(domain, api_key)

        try:
            if method not in ["get", "g", "add", "a", "update", "u", "delete", "del", "d"]:
                print("anxdnsapi: error: Invalid action")
                parser.print_help()
                return 1
            
            if key is None or domain is None:
                print("anxdnsapi: error: No apikey or domain provided")
                parser.print_help()
                return 1

            if verbose:
                print("Using APIKEY: '{}'".format(api_key))
                print("Requesting action: '{}' from {}".format(method, api_url_base))

            methods = {
                "get": self.get,
                "g": self.get,
                "add": self.add,
                "a": self.add,
                "update": self.update,
                "u": self.update,
                "delete": self.delete,
                "d": self.delete,
                "del": self.delete
            }
            
            methods[method](api, args)

        except Exception as e:
            print(e)

        return 0

    def get(self, api, args):
            all_records = api.get_all()
            if args.name is not None:
                print(format_json(api.parse_by_name(all_records, args.name)))
            else:
                print(format_json(all_records))

    def add(self, api, args):
        print("add")
    
    def update(self, api, args):
        print("update")
    
    def delete(self, api, args):
        print("delete")