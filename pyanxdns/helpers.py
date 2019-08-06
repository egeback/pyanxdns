import json


def format_json(data):
    return json.dumps(data, indent=2, sort_keys=True)