from parsers.private.parse_description import parse_description_from_end


def parse_attributes(raw_data: list):
    attributes = list()
    positions_of_attributes = [index for index, key_word in enumerate(raw_data) if key_word == "attribute"]

    for position_of_attr in positions_of_attributes:
        attribute = dict()
        shift = 0
        attribute["type"] = raw_data[position_of_attr + 1]
        if raw_data[position_of_attr + 2] == "[]":
            attribute["array"] = True
            attribute["name"] = raw_data[position_of_attr + 3]
            shift += 1
        else:
            attribute["array"] = False
            attribute["name"] = raw_data[position_of_attr + 2]

        if raw_data[position_of_attr + 3 + shift] == "readonly":
            attribute["readonly"] = True
        else:
            attribute["readonly"] = False

        if "**>" in raw_data[position_of_attr - 1]:
            attribute["description"] = " ".join(parse_description_from_end(raw_data, position_of_attr - 1))


        attributes.append(attribute)
    return attributes
