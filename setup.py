from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FileMonitor',

    version=0.1,

    description='A File Monitor',

    long_description=long_description,

    url='https://github.com/Ldream/FileMonitor',

    author='Ldream',
    author_email='821173262@qq.com',

    license='Apache License',

    keywords='File Monitor',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    install_requires=['watchdog'],

    # List additional groups of dependencies here
    extras_require={},
)
