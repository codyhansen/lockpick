import json


def read_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def write_file(filepath, pass_dict):
    with open(filepath, "w") as f:
        json.dump(pass_dict, f, indent=4)
