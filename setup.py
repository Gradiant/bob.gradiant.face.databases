#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017+ Gradiant, Vigo, Spain

from setuptools import setup, find_packages
from version import *

setup(
    name='bob.gradiant.face.databases',
    version=get_version(),
    description='Public databases interfaces for face recognition and face-PAD',
    url='http://pypi.python.org/pypi/template-gradiant-python',
    license='BSD-3',
    author='Biometrics Team (Gradiant)',
    author_email='biometrics.support@gradiant.org',
    long_description=open('README.md').read(),
    keywords='databases public gradiant',

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,

    install_requires=[
      "setuptools",
    ],

    entry_points={
      'console_scripts': [
        'face_databases_setup_environ.py = bob.gradiant.face.databases.scripts.face_databases_setup_environ:main',
        'face_databases_info.py = bob.gradiant.face.databases.scripts.face_databases_info:main',
        ],
    },
)
