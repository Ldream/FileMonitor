from codecs import open
from os import path

from setuptools import setup, find_packages

import FileMonitor

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FileMonitor',

    version=FileMonitor.__version__,

    description='A File Monitor',

    long_description=long_description,

    url='https://github.com/Ldream/FileMonitor',

    author='Ldream',
    author_email='821173262@qq.com',

    license='Apache License',

    keywords='File Monitor',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    install_requires=['watchdog'],

    # List additional groups of dependencies here
    extras_require={},
)
