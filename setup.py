#!/usr/bin/env python
"""
Utility functions to parse Ardupilot's log file in bin format. 
Contains file converter from Ardupilot's log files in bin format to CSV files.

"""

from setuptools import setup, find_packages

setup(
    name='pybinlog',
    url='https://github.com/tayyabkhalil-313/pybinlog',
    author='Tayyab Khalil',
    author_email='tayyabkhalilpm@gmail.com',
    download_url='https://github.com/tayyabkhalil-313/pybinlog',
    license='MIT License',
    install_requires=['pymavlink'],
    packages=find_packages(),
    version=0.1,
)