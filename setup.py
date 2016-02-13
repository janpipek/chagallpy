#!/usr/bin/env python
from setuptools import setup, find_packages
import chagallpy

setup(
    name='chagallpy',
    version=chagallpy.__version__,
    packages=find_packages(),
    license='MIT',
    description='CHArming GALLEry in PYthon',
    author='Jan Pipek',
    author_email='',
    url='https://github.com/janpipek/chagallpy',
    install_requires = [ 'wowp', 'pillow', "jinja2" ],
    entry_points = {
        'console_scripts' : [
             'chagall = chagallpy:generate'
        ]
    }
)