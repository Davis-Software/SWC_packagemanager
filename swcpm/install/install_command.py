from swcpm import click, swc_pm
from .install_func import install_func


@swc_pm.command("install", short_help="Install a package.")
@click.option("-r", "--reinstall", is_flag=True, help="Re-installs package if it exists. If not, package will be installed normally.")
@click.argument("package", type=click.STRING)
def install(package, reinstall):
    """Install a package.

    \b
    Arguments:
        PACKAGE      name of the package to be download
    """
    install_func(package, reinstall)
