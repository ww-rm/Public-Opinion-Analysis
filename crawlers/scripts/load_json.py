import json


def readjson(address):
    with open(address, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict
