import json
import os
import requests
import platform
from click import echo
from swcpm import constant_packageURL, location_database
from swcpm import constant_defaultAppInstallPATH, constant_defaultModInstallPATH

from swcpm.wget.wget_func import wget_func, extract_archive
from swcpm.remove.remove_command import remove_func


def install_func(package, reinstall, update=False):
    package_url = f"{constant_packageURL}/{package}"
    package_url_json = f"{package_url}/package.json"
    resp = requests.get(package_url_json)
    if resp.status_code != 200:
        echo(f"Specified Package '{package}' does not exist.")
        return
    package_data = resp.json()
    package_file = f"{package_url}/{package_data['id']}.zip"

    if package_data["platforms"] != "all" and platform.system().lower() not in package_data["platforms"]:
        echo("Error: Package is not compatible with your system.")
        return

    install_dir_parent = constant_defaultAppInstallPATH if package_data["type"] in ["cmd", "cmd-f", "app"] else constant_defaultModInstallPATH if "install_dir_override" not in package_data else package_data["install_dir_override"][platform.system().lower()]
    install_dir = os.path.join(install_dir_parent, package)
    install_dir_file = os.path.join(install_dir, f"{package}.zip")
    installed = os.path.exists(os.path.join(install_dir, "package.json"))

    if not installed or (installed and reinstall) or update:
        if reinstall:
            remove_func(package)

        try:
            os.makedirs(install_dir, exist_ok=True)
        except PermissionError:
            echo("Error: Could not create installation directory")
        if not os.access(install_dir, os.W_OK):
            echo(f"PermissionError: Access to this installation path ('{install_dir}') is not permitted")
            return

        with open(os.path.join(install_dir, "package.json"), "w") as f:
            f.write(resp.text)

        echo(f"Downloading Package '{package_file}'")
        wget_func(package_file, install_dir_file)
        echo("Download successful")

        echo(f"Extracting archive '{install_dir_file}'")
        extract_archive(install_dir_file, install_dir)
        echo("Extraction successful")

        os.remove(install_dir_file)
        location_database.set_location(package, install_dir)

        package_requirements = package_data["requirements"]
        if type(package_requirements) == dict:
            for req_type in package_requirements:
                install_packages(package_requirements[req_type], req_type, reinstall)
        elif type(package_requirements) == list:
            if len(package_requirements) > 0:
                echo(f"Additional Packages required: {package_requirements}")
                echo("Installing them all...")
                install_packages(package_requirements, "swcpm", reinstall)
        else:
            echo("Error while parsing Package requirements")
            return

        echo("Installation successful")
    else:
        with open(os.path.join(install_dir, "package.json"), "r") as f:
            pd = json.loads(f.read())
            echo(f"Package '{package}@version{pd['version']}' is already installed")
            if pd["version"] != package_data["version"]:
                echo(f"But can be updated to version '{package_data['version']}' with command: 'swcpm update {package}'")

    echo(f"Package can be run with command: 'swcpm run {package}'")


def install_packages(packages, p_type, reinstall):
    if p_type == "python":
        cmd = ["python" if platform.system() == "win32" else "python3", "-m", "pip", "install"]
        for package in packages:
            cmd.append(package)
        cmd.append("--upgrade")
        os.system(" ".join(cmd))
    elif p_type == "swcpm":
        for package in packages:
            install_func(package, reinstall, update=True)
    else:
        raise Exception("Argument Exception", f"Unknown requirement type: '{p_type}'")
