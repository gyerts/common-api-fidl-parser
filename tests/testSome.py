from . import compare, no_description


def testSome(interface):
    method = interface["methods"][3]
    compare(method["name"], "")
    compare(method["description"], "")

    compare(method["in"][0]["type"], "")
    no_description(method["in"][0])
    compare(method["in"][0]["array"], False)
    compare(method["in"][0]["name"], "")

    compare(method["out"][0]["type"], "")
    no_description(method["out"][0])
    compare(method["out"][0]["array"], False)
    compare(method["out"][0]["name"], "")
