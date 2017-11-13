import os
import json
import glob

from configurations import settings

from parsers.parse_interfaces import parse_interfaces
from parsers.parse_package_name import parse_package_name
from parsers.parse_raw_data import parse_raw_data

from generators.client_generator.generate_hpp_file import generate_file
from generators.client_generator.generate_placeholders import generate_placeholders
from generators.client_generator.generate_types import generate_types
from generators.client_generator.debug_generator import generate_debug_left, generate_debug_right
from generators.client_generator.generate_parametrs import gen_parameters_list

if not os.path.exists("output"):
    os.makedirs("output")

all_files = glob.glob("franca_fidl_files/*.fidl")

if not all_files:
    print("No files found in franca_fidl_files/ directory")
    exit(0)

for file_path in all_files:
    raw_data = parse_raw_data(file_path)

    all = dict()

    #############################
    # Parse package name
    #############################
    all["package_name"] = parse_package_name(raw_data).split(".")
    all["generated_namespace"] = "::".join(all["package_name"])
    all["generated_path"] = "/".join(all["package_name"])

    #############################
    # Parse Interfaces
    #############################
    interfaces = parse_interfaces(raw_data)

    for interface_name, interface_content in interfaces.items():
        all["interface_name"] = interface_name
        all.update(interface_content)

        ##################################################################################################
        # Make required variables for templates
        ##################################################################################################
        for method in interface_content["methods"]:
            generate_types(method, all["interface_name"])
            if "out" in method:
                method["out_placeholders"] = generate_placeholders(method["out"])
                method["out_debug_left"] = generate_debug_left(method["out"])
                method["out_debug_right"] = generate_debug_right(method["out"])
            if "in" in method:
                method["in_params"] = gen_parameters_list(method["in"])
                method["in_debug_left"] = generate_debug_left(method["in"])
                method["in_debug_right"] = generate_debug_right(method["in"])

        ##################################################################################################
        # Generate Client hpp file
        ##################################################################################################
        generate_file(all, all["interface_name"]+".hpp", "template_hpp.txt")

        ##################################################################################################
        # Generate Client cpp file
        ##################################################################################################
        generate_file(all, all["interface_name"]+".cpp", "template_cpp.txt")

        ##################################################################################################
        # Generate Mocks and interface
        ##################################################################################################
        if settings["is_mock"]:
            generate_file(all, all["interface_name"]+"Mock.hpp", "template_mock_hpp.txt")
            generate_file(all, "Interface"+all["interface_name"]+"Client.hpp", "template_interface_hpp.txt")

        ##################################################################################################
        # write to json file read_info.json
        ##################################################################################################
        with open("read_info.json", "w") as f:
            json.dump(all, f, indent=3)
