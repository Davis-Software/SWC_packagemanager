from swcpm.install.install_func import install_func


def update_func(package):
    install_func(package, False, update=True)
