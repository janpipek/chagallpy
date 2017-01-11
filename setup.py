#!/usr/bin/env python
from setuptools import setup, find_packages
import chagallpy

setup(
    name='chagallpy',
    version=chagallpy.__version__,
    packages=find_packages(),
    license='MIT',
    description='CHArming GALLEry in PYthon',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/chagallpy',
    install_requires = [ 'wowp', 'pillow', "jinja2" ],
    entry_points = {
        'console_scripts' : [
             'chagall = chagallpy:generate'
        ]
    },
    include_package_data = True,
    package_data = {
        'resources': ['*.*'],
        'templates': ['*.html']
    },
)
