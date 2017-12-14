def parse_version(raw_data: list):
    version = {
        "major": None,
        "minor": None
    }

    for index, key_word in enumerate(raw_data):
        if "version" == key_word:
            version["major"] = raw_data[index + 3]
            version["minor"] = raw_data[index + 5]
    return version
