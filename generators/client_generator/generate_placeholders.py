def generate_placeholders(params: list):
    placeholders = str()
    for index, param in enumerate(params):
        placeholders += ", std::placeholder::_{}".format(str(index + 1))
    return placeholders
