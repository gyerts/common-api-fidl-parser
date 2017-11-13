def parse_description_from_end(raw_data: list, descr_end: int):
    if "**>" not in raw_data[descr_end]:
        raise AttributeError("The parameter should be '**>' but '{}' given"
                             .format(raw_data[descr_end]))
    descr_start = 0
    while True:
        if "<**" in raw_data[descr_end + descr_start]:
            break
        else:
            descr_start -= 1
    description = raw_data[(descr_end + descr_start):(descr_end + 1)]
    return description


def parse_description_from_start(raw_data: list, descr_start: int):
    if "<**" not in raw_data[descr_start]:
        raise AttributeError("The parameter should be '<**' but '{}' given"
                             .format(raw_data[descr_start]))
    descr_end = 0
    for delta, key_word in enumerate(raw_data[descr_start:]):
        if "**>" in key_word:
            descr_end = descr_start + delta
            break
    description = raw_data[descr_start:descr_end+1]
    return description
