#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import pyCTelebot

setup(
    name='pyCTelebot',
    version=pyCTelebot.__version__,
    packages=find_packages(),
    author='JuanJo78',
    author_email='juanjo78@gmail.com',
    description='pyCTelebot',
    long_description="On github: https://github.com/juanjo78git/pyCTelebot",
    install_requires=[],
    url='https://github.com/juanjo78git/pyCTelebot',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'pyCTelebot = pyCTelebot.pyCTelebotBase:main',
        ],
    },
)
