from setuptools import setup, find_packages

setup(
    name='swcpm',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='Manage Software City Packages',
    download_url='https://github.com/Software-City/SWC_packagemanager/archive/v0.1.tar.gz',
    author="Davis_Software",
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        swcpm=swcpm.main:swc_pm
    ''',
)
