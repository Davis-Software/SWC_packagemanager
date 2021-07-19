from swcpm import click, swc_pm
from .run_func import run_func


@swc_pm.command("run", short_help="Run a package.")
@click.argument("package", type=click.STRING)
def install(package):
    """Run a package.

    \b
    Arguments:
        PACKAGE      name of the package to be run
    """
    run_func(package)
