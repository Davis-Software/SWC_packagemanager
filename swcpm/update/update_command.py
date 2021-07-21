from swcpm import click, swc_pm
from .update_func import update_func


@swc_pm.command("update", short_help="Update a package.")
@click.argument("package", type=click.STRING)
def install(package):
    """Update a package.

    \b
    Arguments:
        PACKAGE      name of the package to be updated
    """
    update_func(package)
