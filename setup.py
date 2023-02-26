#!/usr/bin/env python

from setuptools import setup, find_packages
descr = "Utility functions to parse Ardupilot's log file in bin format. "
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='pybinlog',
    description=descr,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tayyabkhalil-313/pybinlog',
    author='Tayyab Khalil',
    author_email='tayyabkhalilpm@gmail.com',
    download_url='https://github.com/tayyabkhalil-313/pybinlog',
    license='MIT License',
    install_requires=['pymavlink', 'PyQt5'],
    packages=find_packages(),
    version="0.3.4",
    entry_points = {
        'console_scripts': [
            'bin2csv=utils.bin2csv:main',
            'bin2csvgui=utils.bin2csvgui:main',
        ],
    },
)
