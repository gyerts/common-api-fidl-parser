_is_description = False
_description = None


def is_any_description():
    global _description
    return bool(_description)


def pop_description():
    global _is_description
    global _description

    if not _description:
        raise Exception("description empty!")
    
    temp_description = _description.copy()
    _description = None
    return temp_description


def is_description(key_word, save=True):
    global _is_description
    global _description

    if "<**" in key_word:
        _is_description = True
        if save:
            _description = list()
            _description.append(key_word)
        return True

    elif "**>" in key_word:
        _is_description = False
        if save:
            _description.append(key_word)
        return True  # "**>" <- is steal _description
    
    elif _is_description:
        if save:
            _description.append(key_word)

    return _is_description
