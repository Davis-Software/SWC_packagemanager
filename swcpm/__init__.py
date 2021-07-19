import os
import click
import tempfile
import platform
from pathlib import Path
from swcpm.tools.loc_db import LocationDatabase


_param_verbose = False
_param_old_api = False

constant_projectURL = "https://projects.software-city.org/resources"
constant_packageURL = "https://projects.software-city.org/resources/swc_packages"

constant_tempPATH = tempfile.gettempdir()
constant_defaultAppInstallPATH = "C:\\Program Files\\SWC" if platform.system() == "win32" else "/usr/swc"
constant_defaultModInstallPATH = os.path.join(str(Path.home()), "SWC", "Packages")

location_database = LocationDatabase()


def get_option_verbose():
    return _param_verbose


def get_option_old_api():
    return _param_old_api


def verbose_echo(*strings):
    if _param_verbose:
        for string in strings:
            click.echo(string)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Show more info while running.")
@click.option("--old_api", is_flag=True, help="Use old SWC API.")
def swc_pm(verbose, old_api):
    global _param_verbose, _param_old_api

    _param_verbose = verbose
    _param_old_api = old_api
