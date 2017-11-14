def _replace(param: dict, namespace: str):
    if param["type"] == "String":
        param["type"] = "std::string"
    elif param["type"] == "Int32":
        param["type"] = "int32_t"
    elif param["type"] == "Int16":
        param["type"] = "int16_t"
    elif param["type"] == "Int8":
        param["type"] = "int8_t"
    elif param["type"] == "Boolean":
        param["type"] = "bool"
    else:
        param["type"] = "{}::{}".format(namespace, param["type"])


def generate_method_types(method: dict, namespace: str):
    if "in" in method:
        for param in method["in"]:
            _replace(param, namespace)
    if "out" in method:
        for param in method["out"]:
            _replace(param, namespace)
    if "error" in method:
        for param in method["error"]:
            _replace(param, namespace)


def generate_attributes_types(attributes: list, namespace: str):
    for attribute in attributes:
        _replace(attribute, namespace)
