def generate_debug_left(params: list):
    output = str()
    for param in params:
        if param["type"] == "std::string":
            output += " _{}=%s".format(param["name"])
    return output


def generate_debug_right(params: list):
    output = str()
    for param in params:
        if param["type"] == "std::string":
            output += ", _{}.c_str()".format(param["name"])
    return output
