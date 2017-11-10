import re


def _parse_raw_data():
    with open("franca_fidl_files/HelloWorld.fidl") as f:
        dirty_raw_data = re.split(' |\n', f.read())
        dirty_raw_data = [el for el in dirty_raw_data if el != '']

        clean_raw_data = []
        for clean_element in dirty_raw_data:

            def add_if_sign(sign: str, in_element: str, recursively=False):
                added = False
                if sign in in_element and in_element != sign:
                    found_position = in_element.find(sign)

                    left = in_element[:found_position]
                    right = in_element[found_position + 1:]

                    if left:
                        clean_raw_data.append(left)

                    clean_raw_data.append(sign)

                    if sign in right:
                        add_if_sign(sign, right, recursively=True)
                    else:
                        if right: clean_raw_data.append(right)
                    added = True
                elif recursively:
                    if in_element: clean_raw_data.append(in_element)
                return added

            if add_if_sign("{", clean_element):
                continue
            elif add_if_sign("}", clean_element):
                continue
            else:
                if clean_element: clean_raw_data.append(clean_element)

        return clean_raw_data


raw_data = _parse_raw_data()
