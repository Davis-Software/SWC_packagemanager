from .__init__ import click

import requests
from tqdm import tqdm


param_verbose = False
param_old_api = False


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Show more info while running.")
@click.option("--old_api", is_flag=True, help="Use old SWC API.")
def swc_pm(verbose, old_api):
    global param_verbose, param_old_api

    param_verbose = verbose
    param_old_api = old_api


########################################################################################################################


@swc_pm.command("install", short_help="Install a package.")
@click.option("-r", "--reinstall", is_flag=True, help="Re-installs package if it exists. If not, package will be installed normally.")
@click.argument("package", type=click.STRING)
def install(package, reinstall):
    """Install a package.

    \b
    Arguments:
        PACKAGE      name of the package to be download
    """
    click.echo(package, reinstall)


@swc_pm.command("remove", short_help="Remove a package.")
@click.argument("package", type=click.STRING)
def remove(package):
    """Remove a package.

    \b
    Arguments:
        PACKAGE      name of the package to be removed
    """
    click.echo(package)


@swc_pm.command()
@click.argument("url", type=click.STRING)
@click.argument("filename", type=click.STRING)
def wget(url, filename):
    """Like 'wget' in linux.

    \b
    Arguments:
        URL          is the url to the file which should be downloaded
        FILENAME     is the path and name under which the downloaded file is saved
    """
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


if __name__ == '__main__':
    swc_pm()
