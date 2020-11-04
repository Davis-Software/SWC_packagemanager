import requests
from click import echo
from swcpm import constant_packageURL


def get_info(package, raw):
    infoURL = f"{constant_packageURL}/{package}/package.json"
    resp = requests.get(infoURL)
    if resp.status_code == 200:
        data = resp.json()
        if raw:
            return data
        return f"Package ID: {data['id']}\nPackage Type: {data['type']}\nRequired Packages: {data['requirements']}"
    return "Package doesn't exist"


def info_func(package, raw):
    echo(get_info(package, raw))
