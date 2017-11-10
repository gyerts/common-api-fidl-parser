def parse_description(raw_data: list, index_of_end_of_description: int):
    if raw_data[index_of_end_of_description] != "**>":
        raise AttributeError("The parameter should be '**>' but '{}' given"
                             .format(raw_data[index_of_end_of_description]))

    start_of_description = 0
    while True:
        if raw_data[index_of_end_of_description + start_of_description] == "<**":
            break
        else:
            start_of_description -= 1

    return raw_data[(index_of_end_of_description + start_of_description):(index_of_end_of_description + 1)]
