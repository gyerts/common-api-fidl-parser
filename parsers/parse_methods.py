from parsers.private.parse_parameters import parse_in_or_out
from parsers.private.parse_description import parse_description

def parse_methods(raw_data: list):
    method_indexes = [index for index, key_word in enumerate(raw_data) if key_word == 'method']

    methods = []

    for method_index in method_indexes:
        method = {
            "name": raw_data[method_index+1]
        }
        if raw_data[method_index+2] != "{":
            raise Exception("incorrect index of method start brace, but in this position "
                            "key word \"{}\"".format(raw_data[method_index+3]))

        ########################################################
        #                  PARSE IN/OUT/ERROR
        ########################################################
        entries = 0
        for delta, key_word in enumerate(raw_data[method_index:]):
            if key_word == "{":
                entries += 1
                continue
            if key_word == "}":
                entries -= 1
                if entries == 0:
                    break

            if key_word == "in":
                method["in"] = parse_in_or_out(raw_data, method_index + delta + 1, "in")
            if key_word == "out":
                method["out"] = parse_in_or_out(raw_data, method_index + delta + 1, "out")
            if key_word == "error":
                method["error"] = parse_in_or_out(raw_data, method_index + delta + 1, "error")

        ########################################################
        #                  PARSE DESCRIPTION
        ########################################################
        if raw_data[method_index-1] == "**>":
            method["description"] = parse_description(raw_data, method_index-1)

        methods.append(method)
    return methods
