import os
import click
import platform
from distutils.dir_util import copy_tree


exec_dir = os.path.dirname(os.path.realpath(__file__))


def deploy_func(path):
    os.makedirs(path, exist_ok=True)
    if not os.access(path, os.W_OK):
        click.echo(f"Not enough permissions to access path '{path}'")
        return
    
    copy_tree(
        os.path.join(exec_dir, "app"),
        path
    )
    click.echo("Deployed instance successfully")


def run_func(path):
    if not (os.path.exists(os.path.join(path, "main.py")) and os.path.exists(os.path.join(path, "server_files"))):
        ctx = click.get_current_context()
        click.echo(f"No instance in given directory: '{os.path.abspath(path)}'")
        click.echo(ctx.get_help())
        ctx.exit()
        return

    os.chdir(path)
    os.system(" ".join(
        [
            "python" if platform.system() == "win32" else "python3",
            os.path.join(path, "main.py"),
        ]
    ))


@click.command()
@click.option("-d", "--deploy", is_flag=True, help="Deploy new instace")
@click.argument("path", default=".", type=click.Path())
def main_cmd(deploy, path):
    """Run or deploy a flaskDebuggingServerApp instance

    \b
    Arguments:
        PATH      path to the instance directory (Default: Current directory)
    """

    if path == ".":
        path = os.path.abspath(path)

    if deploy:
        deploy_func(path)
    else:
        run_func(path)


if __name__ == "__main__":
    main_cmd()
