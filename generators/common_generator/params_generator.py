import re


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


# add str "const std::string &_s1, const std::string &_s2"
def generate_params_ctrn(params: list):
    output = str()
    if params:
        last_param = params[-1]
        for param in params:
            if param == last_param:
                output += "const {type} &_{name}".format(type=param["type"], name=param["name"])
            else:
                output += "const {type} &_{name}, ".format(type=param["type"], name=param["name"])
    return output


# add str "std::string &_s1, std::string &_s2"
def generate_params_trn(params: list):
    output = str()
    if params:
        last_param = params[-1]
        for param in params:
            if param == last_param:
                output += "{type} &_{name}".format(type=param["type"], name=param["name"])
            else:
                output += "{type} &_{name}, ".format(type=param["type"], name=param["name"])
    return output


# add str "std::string _s1, std::string _s2"
def generate_params_tn(params: list):
    output = str()
    if params:
        last_param = params[-1]
        for param in params:
            if param == last_param:
                output += "const {type} _{name}".format(type=param["type"], name=param["name"])
            else:
                output += "const {type} _{name}, ".format(type=param["type"], name=param["name"])
    return output


# add str "_s1, _s2"
def generate_params_n(params: list):
    output = str()
    if params:
        last_param = params[-1]
        for param in params:
            if param == last_param:
                output += "_{name}".format(name=param["name"])
            else:
                output += "_{name}, ".format(name=param["name"])
    return output


# add str "_s1, _s2, "
def generate_params_nr(params: list):
    output = str()
    for param in params:
        output += "_{name}, ".format(name=param["name"])
    return output


# add str ", _s1, _s2"
def generate_params_nl(params: list):
    output = str()
    for param in params:
        output += ", _{name}".format(name=param["name"])
    return output


# add str "std::placeholders::_1, std::placeholders::_2"
def generate_params_placeholders_n(params: list):
    output = str()
    if params:
        last_param = params[-1]
        for index, param in enumerate(params):
            if param == last_param:
                output += "std::placeholders::_{index}".format(index=index+2)
            else:
                output += "std::placeholders::_{index}, ".format(index=index+2)
    return output


# add str ", std::placeholders::_1, std::placeholders::_2"
def generate_params_placeholders_nl(params: list, minus: int = 0):
    output = str()
    for index, param in enumerate(params):
        output += ", std::placeholders::_{index}".format(index=index + 2 - minus)
    return output


# add str "std::placeholders::_1, std::placeholders::_2, "
def generate_params_placeholders_nr(params: list):
    output = str()
    for index, param in enumerate(params):
        output += "std::placeholders::_{index}, ".format(index=index + 2)
    return output


# add str ", std::placeholders::_1, std::placeholders::_2, "
def generate_params_placeholders_nb(params: list):
    output = str()
    if params:
        last_param = params[-1]
        first_param = params[0]
        for index, param in enumerate(params):
            if param == first_param:
                output += ", std::placeholders::_{index}".format(index=index + 2)
            elif param == last_param:
                output += ", std::placeholders::_{index}, ".format(index=index+2)
            else:
                output += ", std::placeholders::_{index}".format(index=index+2)
    return output


## TODO: better replace with using "inflection.underscore('CamelCase')" library
def convert_camelcase_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
