import shutil
from click import echo
from swcpm import location_database


def remove_func(package):
    install_dir = location_database.get_location(package)
    if not install_dir:
        echo(f"Package '{package}' is not installed")
        return

    shutil.rmtree(install_dir)
    location_database.remove_location(package)
