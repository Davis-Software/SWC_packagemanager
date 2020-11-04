from swcpm import click, swc_pm
from .info_func import info_func


@swc_pm.command("info", short_help="Get info about a package.")
@click.option("-r", "--raw", is_flag=True, help="Gives back raw data.")
@click.argument("package", type=click.STRING)
def install(package, raw):
    """Get info about a package.

    \b
    Arguments:
        PACKAGE      name of the package to get info about.
    """
    info_func(package, raw)
