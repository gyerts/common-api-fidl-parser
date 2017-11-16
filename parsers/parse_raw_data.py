import re


def parse_raw_data(filename):
    with open(filename) as f:
        dirty_raw_data = f.read()
        dirty_raw_data = dirty_raw_data.replace("{}", "{ }")
        dirty_raw_data = re.split(' |\n', dirty_raw_data)
        dirty_raw_data = [el for el in dirty_raw_data if el != '']

        clean_raw_data = []
        for clean_element in dirty_raw_data:

            def add_if_sign(sign: str, in_element: str, recursively=False):
                added = False
                if sign in in_element and in_element != sign:
                    found_position = in_element.find(sign)

                    left = in_element[:found_position]
                    center = in_element[found_position:found_position+len(sign)]
                    right = in_element[found_position+len(sign):]

                    if left: clean_raw_data.append(left)

                    if center != sign: raise Exception("logic error: {} != {}".format(center, sign))
                    else: clean_raw_data.append(sign)

                    if right: clean_raw_data.append(right)

                    if sign in right:
                        add_if_sign(sign, right, recursively=True)
                    else:
                        if right: clean_raw_data.append(right)

                    added = True
                elif recursively:
                    if in_element: clean_raw_data.append(in_element)
                return added

            key_words_to_split = ["{", "}", "<**", "**>"]
            for key_word_to_split in key_words_to_split:
                if add_if_sign(key_word_to_split, clean_element):
                    break
            else:
                if "" != clean_element:
                    clean_raw_data.append(clean_element)
        return clean_raw_data
