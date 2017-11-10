def parse_interface_name(raw_data: list):
    interface_index = raw_data.index("interface")
    return raw_data[interface_index+1]
