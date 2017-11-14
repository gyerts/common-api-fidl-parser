"""
generates next
    "function_1, function_2, function_n, "
"""


def gen_parameters_list(params: list):
    output = str()
    for param in params:
        output += "_{}, ".format(param["name"])
    return output
