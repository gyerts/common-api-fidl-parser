import glob
import json
import os

from configurations import settings
from generators.common_generator.render_file import generate_file
from generators.common_generator.debug_generator import generate_debug_left, generate_debug_right
from generators.common_generator.generate_parametrs import gen_parameters_list
from generators.common_generator.generate_placeholders import generate_placeholders
from generators.common_generator.generate_types import generate_method_types
from generators.common_generator.generate_types import generate_attributes_types
from parsers.parse_interfaces import parse_interfaces
from parsers.parse_package_name import parse_package_name
from parsers.parse_raw_data import parse_raw_data
from generators.common_generator.render_file import set_template_dir

# Capture our current directory
set_template_dir(os.path.dirname(os.path.abspath(__file__)))

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
        generate_attributes_types(interface_content["attributes"], all["interface_name"])
        for method in interface_content["methods"]:
            generate_method_types(method, all["interface_name"])
            if "out" in method:
                method["out_placeholders"] = generate_placeholders(method["out"])
                method["out_debug_left"] = generate_debug_left(method["out"])
                method["out_debug_right"] = generate_debug_right(method["out"])
            if "in" in method:
                method["in_params"] = gen_parameters_list(method["in"])
                method["in_debug_left"] = generate_debug_left(method["in"])
                method["in_debug_right"] = generate_debug_right(method["in"])

        for broadcast in interface_content["broadcasts"]:
            generate_method_types(broadcast, all["interface_name"])
            if "out" in broadcast:
                broadcast["out_placeholders"] = generate_placeholders(broadcast["out"])
                broadcast["out_debug_left"] = generate_debug_left(broadcast["out"])
                broadcast["out_debug_right"] = generate_debug_right(broadcast["out"])

        ##################################################################################################
        # Generate Client
        ##################################################################################################
        # generate_file(all, "C"+all["interface_name"]+"Client.hpp", "templates/client/template_hpp.txt")
        # generate_file(all, "C"+all["interface_name"]+"Client.cpp", "templates/client/template_cpp.txt")
        # if settings["is_mock"]:
        #     generate_file(all, "C"+all["interface_name"]+"ClientMock.hpp", "templates/client/template_mock_hpp.txt")
        #     generate_file(all, "Interface"+all["interface_name"]+"Client.hpp", "templates/client/template_interface_hpp.txt")
        #
        ##################################################################################################
        # Generate Server
        ##################################################################################################
        generate_file(all, "C" + all["interface_name"] + "Server.hpp", "templates/server/template_hpp.txt")
        generate_file(all, "C" + all["interface_name"] + "Server.cpp", "templates/server/template_cpp.txt")
        if settings["is_mock"]:
            generate_file(all, "C" + all["interface_name"] + "ServerMock.hpp", "templates/server/template_mock_hpp.txt")
            generate_file(all, "Interface" + all["interface_name"] + "Server.hpp",
                          "templates/server/template_interface_hpp.txt")

        ##################################################################################################
        # write to json file read_info.json
        ##################################################################################################
        with open("read_info.json", "w") as f:
            json.dump(all, f, indent=3)
