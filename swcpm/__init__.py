import os
import json
import click
import tempfile
import platform
from pathlib import Path


class LocationDatabase:
    database_dir = os.path.join(str(Path.home()), "SWC", "database")
    database_path = os.path.join(database_dir, "locations.json")

    def __init__(self):
        if not os.path.exists(self.database_path):
            os.makedirs(self.database_dir, exist_ok=True)
            with open(self.database_path, "w") as f:
                f.write("{}")

        with open(self.database_path, "r") as f:
            self.locations = json.loads(f.read())

    def __update(self):
        with open(self.database_path, "w") as f:
            f.write(json.dumps(self.locations))

    def get_location(self, package):
        try:
            return self.locations[package]
        except KeyError:
            return None

    def set_location(self, package, location):
        self.locations[package] = location
        self.__update()

    def remove_location(self, package):
        del self.locations[package]
        self.__update()


_param_verbose = False

constant_projectURL = "https://projects.software-city.org/resources"
constant_packageURL = "https://projects.software-city.org/resources/swc_packages"

constant_tempPATH = tempfile.gettempdir()
constant_defaultAppInstallPATH = "C:\\Program Files\\SWC" if platform.system() == "win32" else "/usr/swc"
constant_defaultModInstallPATH = os.path.join(str(Path.home()), "SWC", "Packages")

location_database = LocationDatabase()


def get_option_verbose():
    return _param_verbose


def verbose_echo(*strings):
    if _param_verbose:
        for string in strings:
            click.echo(string)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Show more info while running.")
def swc_pm(verbose):
    global _param_verbose

    _param_verbose = verbose
