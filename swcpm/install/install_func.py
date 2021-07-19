import json
import os
import requests
import platform
from click import echo
from swcpm import constant_packageURL, location_database
from swcpm import constant_defaultAppInstallPATH, constant_defaultModInstallPATH

from swcpm.wget.wget_func import wget_func, extract_archive


def install_func(package, reinstall):
    package_url = f"{constant_packageURL}/{package}"
    package_url_json = f"{package_url}/package.json"
    resp = requests.get(package_url_json)
    package_data = resp.json()
    package_file = f"{package_url}/{package_data['id']}.zip"

    if package_data["platforms"] != "all" and platform.system().lower() not in package_data["platforms"]:
        echo("Error: Package is not compatible with your system.")
        return

    install_dir_parent = constant_defaultAppInstallPATH if package_data["type"] in ["cmd", "cmd-f", "app"] else constant_defaultModInstallPATH if "install_dir_override" not in package_data else package_data["install_dir_override"][platform.system().lower()]
    install_dir = os.path.join(install_dir_parent, package)
    install_dir_file = os.path.join(install_dir, f"{package}.zip")
    installed = os.path.exists(os.path.join(install_dir, "package.json"))

    if not installed or (installed and reinstall):
        # if not os.access(install_dir, 1):
        #     echo(f"PermissionError: Access to this installation path ('{install_dir}') is not permitted")
        #     return

        os.makedirs(install_dir, exist_ok=True)
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
        echo("Installation successful")
    else:
        with open(os.path.join(install_dir, "package.json"), "r") as f:
            pd = json.loads(f.read())
            echo(f"Package '{package}@version{pd['version']}' is already installed")
            if pd["version"] != package_data["version"]:
                echo(f"But can be updated to version '{package_data['version']}' with command: 'swcpm update {package}'")

    echo(f"Package can be run with command: 'swcpm run {package}'")

