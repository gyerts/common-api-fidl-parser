from parsers.private.parse_parameters import parse_in_or_out
from parsers.private.parse_description import parse_description_from_end
from parsers.helpers import is_description


def parse_broadcasts(raw_data: list):
    broadcast_indexes = []
    for index, key_word in enumerate(raw_data):
        if not is_description(key_word) and key_word == 'broadcast':
            broadcast_indexes.append(index)

    broadcasts = []

    for broadcast_index in broadcast_indexes:
        shift = 0
        broadcast = {
            "name": raw_data[broadcast_index+1]
        }
        if "selective" == raw_data[broadcast_index + 2]:
            broadcast["selective"] = True
            shift += 1
        else:
            broadcast["selective"] = False

        if raw_data[broadcast_index+2+shift] != "{":
            print(raw_data[broadcast_index:broadcast_index+3+20])
            raise Exception("incorrect index of broadcast \"{}\" start brace, but in this position "
                            "key word \"{}\"".format(broadcast["name"], raw_data[broadcast_index+3]))

        ########################################################
        #                  PARSE IN/OUT/ERROR
        ########################################################
        entries = 0
        cut_raw_data = raw_data[broadcast_index:]
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
            if key_word == "out":
                broadcast["out"] = parse_in_or_out(raw_data, broadcast_index + delta + 1, "out")
        
        ########################################################
        #                  PARSE DESCRIPTION
        ########################################################
        if "**>" in raw_data[broadcast_index - 1]:
            broadcast["description"] = " ".join(parse_description_from_end(raw_data, broadcast_index - 1))

        broadcasts.append(broadcast)
    return broadcasts
