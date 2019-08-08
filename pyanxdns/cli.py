import argparse
import os
from functools import partial
from .core import API
from .core import api_url_base
from .helpers import format_json


def add_base_arguments(parser, key, domain):
    parser.add_argument("-k", "--apikey", required=False, help="API key used in request header", default=key)
    parser.add_argument("-d", "--domain", required=False, help="Domain name", default=domain)
    parser.add_argument("-v", "--verbose", required=False, help="Verbose", default=False, action='store_true')

def add_extended_arguments(parser, key, domain):
    parser.add_argument('-t', '--ttl', required=False, help='Time to live parameter', default=3600, type=int)

def add_get_parsers(subparsers, key, domain):
    parser_get = subparsers.add_parser('get', help='Get records', aliases=['g'])
    parser_get.add_argument('-n', '--name', required=False, help='Name parameter', default=None)

    add_base_arguments(parser_get, key, domain)

def add_add_parsers(subparsers, key, domain):
    parser_add = subparsers.add_parser('add', help='Add record', aliases=['a'])
    parser_record_type = parser_add.add_subparsers(title='Record type', help='Record type to add', dest="type")
    
    parser_txt = parser_record_type.add_parser('txt', help='Txt record', aliases=["TXT"])
    parser_a = parser_record_type.add_parser('a', help='A record', aliases=["A"])
    parser_cname = parser_record_type.add_parser('cname', help='CNAME record', aliases=["A"])

    parser_txt.add_argument("name", help='Record name')
    parser_txt.add_argument("txt", help='Record txt')
    parser_a.add_argument("name", help='Record name')
    parser_a.add_argument("address", help='Record address')
    parser_cname.add_argument("name", help='Record name')
    parser_cname.add_argument("address", help='Record address')

    parsers = [parser_add, parser_txt, parser_a, parser_cname]

    for p in parsers:
        add_base_arguments(p, key, domain)
        add_extended_arguments(p, key, domain)

def add_update_parsers(subparsers, key, domain):
    parser_update = subparsers.add_parser('update', help='Update record', aliases=['u'])
    parser_update.add_argument('-l', '--line', required=False, help='line parameter', default=None)

    parser_record_type = parser_update.add_subparsers(title='Record type', help='Record type to add', dest="type")
    
    parser_txt = parser_record_type.add_parser('txt', help='Txt record', aliases=["TXT"])
    parser_a = parser_record_type.add_parser('a', help='A record', aliases=["A"])
    parser_cname = parser_record_type.add_parser('cname', help='CNAME record', aliases=["CNAME"])

    parser_txt.add_argument("-n", "--name", help='Record name')
    parser_txt.add_argument("-r", "--line", help='Record line')
    parser_txt.add_argument("txt", help='Record txt')

    parser_a.add_argument("-r", "--line", help='Record line')
    parser_a.add_argument("-n", "--name", help='Record name')
    parser_a.add_argument("address", help='Record address')
    parser_cname.add_argument("-r", "--line", help='Record line')
    parser_cname.add_argument("-n", "--name", help='Record name')
    parser_cname.add_argument("address", help='Record address')

    parsers = [parser_update, parser_txt, parser_a, parser_cname]

    for p in parsers:
        add_base_arguments(p, key, domain)

def add_delete_parsers(subparsers, key, domain):
    parser_delete = subparsers.add_parser('delete', help='Delete record', aliases=['d', 'del'])
    parser_delete.add_argument('-r', '--line', required=False, help='Line parameter', default=None)
    parser_delete.add_argument('-n', '--name', required=False, help='Name parameter', default=None)


class CLI:
    def start(self, *param):
        parser = argparse.ArgumentParser()
        key = os.environ['ANXDNS_APIKEY'] if 'ANXDNS_APIKEY' in os.environ else None
        domain = os.environ['ANXDNS_DOMAIN'] if 'ANXDNS_DOMAIN' in os.environ else None
        
        subparsers = parser.add_subparsers(title='Actions', help='Action to perform', dest="action")
        add_base_arguments(parser, key, domain)

        add_get_parsers(subparsers, key, domain)
        add_add_parsers(subparsers, key, domain)
        add_update_parsers(subparsers, key, domain)
        add_delete_parsers(subparsers, key, domain)

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
            
            if api_key is None or api_key is "" or domain is None:
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
        ttl = args.ttl if 'ttl' in args else 3600
        record_type = args.type
        
        method = {
            "txt": partial(api.add_txt_record, args.name, args.txt if 'txt' in args else "", ttl=ttl),
            "cname": partial(api.add_cname_record, args.name, args.address if 'address' in args else "", ttl=ttl),
            "a": partial(api.add_a_record, args.name, args.address if 'address' in args else "", ttl=ttl)
        }
        
        print("add")
        method[record_type.lower()]()
    
    def update(self, api, args):
        ttl = args.ttl if 'ttl' in args else 3600
        record_type = args.type
        txt = args.name if 'txt' in args else None
        address = args.name if 'address' in args else None
        name = args.name if 'name' in args else None
        line = args.line if 'line' in args else None
        
        method = {
            "txt": partial(api.update_txt_record, txt, name=name, ttl=ttl, line=line),
            "cname": partial(api.update_cname_record, address, name=name, line=line, ttl=ttl),
            "a": partial(api.update_a_record, address, name=name, line=line, ttl=ttl)
        }

        method[record_type.lower()]()

        print("update")
    
    def delete(self, api, args):
        print("delete")