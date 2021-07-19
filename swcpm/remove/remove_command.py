from swcpm import click, swc_pm
from .remove_func import remove_func


@swc_pm.command("remove", short_help="Install a package.")
@click.argument("package", type=click.STRING)
def install(package):
    """Remove a package.

    \b
    Arguments:
        PACKAGE      name of the package to be removed
    """
    remove_func(package)
