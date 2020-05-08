#!/usr/bin/env python
# Copyright 2020 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='xfile',
    version='0.1.0',
    description='Multi-source file information',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Juan Mera',
    author_email='juanmera@gmail.com',
    url='https://www.github.com/juanmera/xfile',
    packages=['xfile', 'xfile.plugin'],
    install_requires=['python-magic',
                      'binwalk @ git+https://github.com/ReFirmLabs/binwalk.git@v2.2.0#egg=binwalk',
                      'rads2file @ git+https://github.com/juanmera/rads2file.git#egg=rads2file'
    ],
    entry_points={ 'console_scripts': ['xfile=xfile.main:main'] }
)
