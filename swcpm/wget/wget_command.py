from swcpm import click, swc_pm
from .wget_func import wget_func


@swc_pm.command()
@click.option("-n", "-f", "--filename", type=click.Path(), help="Custom path and name under which the downloaded file is saved")
@click.argument("url", type=click.STRING)
def wget(url, filename):
    """Like 'wget' in linux.

    \b
    Arguments:
        URL          is the url to the file which should be downloaded
    """
    name = filename or url.split("/")[-1]
    wget_func(url, name)
