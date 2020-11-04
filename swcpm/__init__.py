import click
import tempfile
import platform


param_verbose = False
param_old_api = False

constant_projectURL = "https://projects.software-city.org/resources"
constant_packageURL = "https://projects.software-city.org/resources/swc_packages"

constant_tempPATH = tempfile.gettempdir()
constant_defaultInstallPATH = "C:\\Program Files" if platform.system() == "win32" else "/usr"


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Show more info while running.")
@click.option("--old_api", is_flag=True, help="Use old SWC API.")
def swc_pm(verbose, old_api):
    global param_verbose, param_old_api

    param_verbose = verbose
    param_old_api = old_api
