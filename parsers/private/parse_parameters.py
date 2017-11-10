def parse_in_or_out(raw_data: list, index_of_open_brace: int, in_or_out: str):
    if raw_data[index_of_open_brace] != "{":
        raise AttributeError("index_of_open_brace don't match '{' -> '{}' instead"
                             .format(raw_data[index_of_open_brace]))

    if raw_data[index_of_open_brace - 1] != in_or_out:
        raise AttributeError("index_of_open_brace -1 don't match '{}' -> '{}' instead"
                             .format(in_or_out, raw_data[index_of_open_brace - 1]))

    # STATES
    FIRST, SECOND = 0, 1
    ACTIVE_STATE = 0
    NOT_ADDED = False

    entries = 0

    parameters = list()

    for key_word in raw_data[index_of_open_brace:]:

        if key_word == "{":
            entries += 1
            continue
        if key_word == "}":
            entries -= 1
            if NOT_ADDED:
                parameters.append(MEMBER)
                NOT_ADDED = False
            if 0 == entries:
                break

        if ACTIVE_STATE == FIRST:
            MEMBER = dict()
            MEMBER["list"] = False
            NOT_ADDED = True
            MEMBER["type"] = key_word
            ACTIVE_STATE += 1

        elif ACTIVE_STATE == SECOND:
            if key_word == "[]":
                MEMBER["list"] = True
            else:
                MEMBER["name"] = key_word
                if NOT_ADDED:
                    parameters.append(MEMBER)
                    NOT_ADDED = False
                ACTIVE_STATE = FIRST
    return parameters
