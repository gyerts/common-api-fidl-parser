def parse_package_name(raw_data: list):
    package_name = None
    for index, key_word in enumerate(raw_data):
        if "package" == key_word:
            package_name = raw_data[index + 1]
    return package_name