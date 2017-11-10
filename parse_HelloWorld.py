import os
import sys

from parsers.parse_raw_data import raw_data
print(raw_data)

from parsers.parse_interface_name import parse_interface_name
interface_name = parse_interface_name(raw_data)
print(interface_name)

from parsers.parse_methods import parse_methods
all_methods = parse_methods(raw_data)
print("ALL METHODS ================================================")
for method in all_methods:
    print("======================")
    print(method["name"])
    if "in"          in method: print("[IN]    ",       method["in"])
    if "out"         in method: print("[OUT]   ",       method["out"])
    if "error"       in method: print("[ERROR] ",       method["error"])
    if "description" in method: print("[DESCRIPTION] ", method["description"])

from parsers.parse_broadcasts import parse_broadcasts
all_broadcasts = parse_broadcasts(raw_data)
print("ALL BROADCASTS ================================================")
for broadcast in all_broadcasts:
    print("======================")
    print(broadcast["name"])
    if "out"         in broadcast: print("[OUT] ",         broadcast["out"])
    if "description" in broadcast: print("[DESCRIPTION] ", broadcast["description"])


import json

all = dict()

all["methods"] = all_methods
all["broadcasts"] = all_broadcasts

with open("read_info.json", "w") as f:
    json.dump(all, f, indent=4)
