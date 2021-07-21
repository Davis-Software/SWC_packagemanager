from swcpm import click, swc_pm

from .run import run_command
from .info import info_command
from .wget import wget_command
from .install import install_command
from .update import update_command
from .remove import remove_command


########################################################################################################################


@swc_pm.command("debug", short_help="Debugs the application.")
def debug():
    """Debugs the application."""
    cmd_list = [run_command, info_command, wget_command, install_command, update_command, remove_command]
    for cmd in cmd_list:
        click.echo("Found command module: " + cmd.__name__)


if __name__ == '__main__':
    swc_pm()
