def compare(str1, str2):
    if str1 != str2: raise Exception("{} != {}".format(str1, str2))

def no_description(scope: dict):
    if "description" in scope:
        raise Exception("Should be no description, but description given:\n{}".format(scope["description"]))
