import requests
from click import echo
from swcpm import constant_packageURL, get_option_verbose

possible_arguments = {
    "id": {"required": True, "name": "Package ID", "display": True},
    "type": {"required": True, "name": "Package Type", "display": False},
    "version": {"required": True, "name": "Package Version", "display": True},
    "exec": {"required": True, "name": "Package Main", "display": False},
    "requirements": {"required": False, "name": "Package Requirements", "display": True},
    "platforms": {"required": True, "name": "Compatible Platforms", "display": True},
    "install_dir_override": {"required": False, "name": "Package Installation Location", "display": True}
}


def format_type(var):
    var_type = type(var)
    if var_type in [str, int, bool, float]:
        if var == "null":
            return "none"
        return str(var)
    elif var_type == list:
        if not var:
            return "none"
        return " / ".join(var)
    elif var_type == dict:
        rt = str()
        for key in var:
            rt += f"\n    {key}: '{var[key]}'"
        return rt
    else:
        return var


def data_builder(package, data):
    return_str = str()
    for argument in possible_arguments:
        if possible_arguments[argument]["required"] and argument not in data:
            return f"Error: Package '{package}' has an invalid structure\n(Missing component '{argument}' in its 'package.json')"
        if argument in data and (possible_arguments[argument]["display"] or get_option_verbose()):
            return_str += f"{possible_arguments[argument]['name']}: {format_type(data[argument])}\n"
    return return_str


def get_info(package, raw):
    infoURL = f"{constant_packageURL}/{package}/package.json"
    resp = requests.get(infoURL)
    if resp.status_code == 200:
        data = resp.json()
        if raw:
            return data
        return data_builder(package, data)
    return "Package doesn't exist"


def info_func(package, raw):
    echo(get_info(package, raw))
