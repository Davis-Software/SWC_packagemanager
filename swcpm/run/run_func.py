import os
import json
import platform
from click import echo
from swcpm import location_database


def run_func(package, args):
    install_dir = location_database.get_location(package)
    if not install_dir:
        echo(f"Package '{package}' is not installed")
        return

    install_dir_file = os.path.join(install_dir, "package.json")

    with open(install_dir_file, "r") as f:
        package_data = json.loads(f.read())

    execution_type = package_data["type"]
    execution_target = package_data["exec"]

    if execution_type in ["cmd", "cmd-f", "app"]:
        os.system(execution_target)
    elif execution_type == "python":
        arg_li = list()
        for arg in args:
            arg_li.append(arg)
        os.system(f"{'python' if platform.system() == 'win32' else 'python3'} {os.path.join(install_dir, execution_target)}.py " + " ".join(arg_li))
    else:
        echo(f"Unknown package type: '{execution_type}' - Target '{execution_target}' is not executable")
