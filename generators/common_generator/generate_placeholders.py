"""
generates next
    ", std::placeholder::_1, std::placeholder::_2, std::placeholder::_n"
"""


def generate_placeholders(params: list):
    placeholders = str()
    for index, param in enumerate(params):
        placeholders += ", std::placeholder::_{}".format(str(index + 1))
    return placeholders
