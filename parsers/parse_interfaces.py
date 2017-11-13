from parsers.parse_methods import parse_methods
from parsers.parse_broadcasts import parse_broadcasts
from parsers.parse_attributes import parse_attributes
from parsers.parse_interface_name import parse_interface_name
from parsers.helpers import is_description


def define_scope(raw_data: list, start_position: int):
    found_start_braces = 0
    count_started = False
    delta = start_position
    for key_word in raw_data[start_position:]:
        if "{" == key_word:
            found_start_braces += 1
            count_started = True
        if "}" == key_word:
            found_start_braces -= 1
        if count_started and found_start_braces == 0:
            break
        delta += 1
    return (start_position, delta,)


def get_interfaces_position(raw_data: list):
    all_interfaces_start_points = []
    for index, key_word in enumerate(raw_data):
        if not is_description(key_word) and key_word == "interface":
            all_interfaces_start_points.append(index)

    interfaces_diaposons = []
    for start_point in all_interfaces_start_points:
        interfaces_diaposons.append(define_scope(raw_data, start_point))
    return interfaces_diaposons


def parse_interfaces(raw_data: list):
    interfaces = dict()
    interfaces_position = get_interfaces_position(raw_data)

    #############################
    # Add methods
    #############################

    for start_pos, end_pos in interfaces_position:
        interface_raw_data = raw_data[start_pos:end_pos+1]

        interface_name = parse_interface_name(interface_raw_data)
        interfaces[interface_name] = dict()

        interfaces[interface_name]["methods"] = parse_methods(interface_raw_data)
        interfaces[interface_name]["broadcasts"] = parse_broadcasts(interface_raw_data)
        interfaces[interface_name]["attributes"] = parse_attributes(interface_raw_data)
    return interfaces
