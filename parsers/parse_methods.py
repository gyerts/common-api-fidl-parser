from parsers.private.parse_parameters import parse_in_or_out
from parsers.private.parse_description import parse_description_from_end
from parsers.helpers import is_description


def parse_methods(raw_data: list):
    method_indexes = []
    for index, key_word in enumerate(raw_data):
        if not is_description(key_word) and key_word == 'method':
            method_indexes.append(index)

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
        cut_raw_data = raw_data[method_index:]
        for delta, key_word in enumerate(cut_raw_data):
            if is_description(key_word, save=False):
                continue

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
        if "**>" in raw_data[method_index-1]:
            method["description"] = " ".join(parse_description_from_end(raw_data, method_index - 1))

        methods.append(method)
    return methods
