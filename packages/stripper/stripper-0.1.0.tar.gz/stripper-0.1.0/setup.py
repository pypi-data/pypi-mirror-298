# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='stripper',  # Package name (choose a unique one)
    version='0.1.0',  # Initial version
    author='Abinesh',
    author_email='abineshrseasense@gmail.com',
    description='A simple utility to strip text after a semicolon',
    long_description=open('README.md').read(),  # Contents of README.md as long description
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically finds the package in stripper/
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

