from setuptools import setup, find_packages


with open("./README.md", "r") as rm:
    long_desc = rm.read()


setup(
    name='swcpm',
    version='0.1.6',
    packages=find_packages(),
    license='MIT',
    description='Manage Software City Packages',
    download_url='https://github.com/Software-City/SWC_packagemanager/archive/v0.1.2.tar.gz',
    url='https://github.com/Software-City/SWC_packagemanager',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="davis_software",
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'tqdm'
    ],
    entry_points={
        "console_scripts": [
            "swcpm=swcpm.main:swc_pm"
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
