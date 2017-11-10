from parsers.private.parse_parameters import parse_in_or_out
from parsers.private.parse_description import parse_description


def parse_broadcasts(raw_data: list):
    broadcast_indexes = [index for index, key_word in enumerate(raw_data) if key_word == 'broadcast']

    broadcasts = []

    for broadcast_index in broadcast_indexes:
        broadcast = {
            "name": raw_data[broadcast_index+1]
        }
        if raw_data[broadcast_index+3] != "{":
            raise Exception("incorrect index of broadcast start brace, but in this position "
                            "key word \"{}\"".format(raw_data[broadcast_index+3]))

        ########################################################
        #                  PARSE IN/OUT/ERROR
        ########################################################
        entries = 0
        for delta, key_word in enumerate(raw_data[broadcast_index:]):
            if key_word == "{":
                entries += 1
                continue
            if key_word == "}":
                entries -= 1
                if entries == 0:
                    break
            if key_word == "out":
                broadcast["out"] = parse_in_or_out(raw_data, broadcast_index + delta + 1, "out")
        
        ########################################################
        #                  PARSE DESCRIPTION
        ########################################################
        if raw_data[broadcast_index - 1] == "**>":
            broadcast["description"] = parse_description(raw_data, broadcast_index - 1)

        broadcasts.append(broadcast)
    return broadcasts
