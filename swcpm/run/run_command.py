from swcpm import click, swc_pm
from .run_func import run_func


@swc_pm.command("run", short_help="Run a package.", context_settings={"ignore_unknown_options": True})
@click.argument("package", type=click.STRING, nargs=1)
@click.argument("args", type=click.STRING, nargs=-1)
def install(package, args):
    """Run a package.

    \b
    Arguments:
        PACKAGE      name of the package to be run
        ARGS         arguments that are to be passed on to the requested package on execution (cannot be --help)
    """
    run_func(package, args)
