# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='stripper',
    version='0.1.5',  # Increment the version here
    author='Abinesh',
    author_email='abineshrseasense@gmail.com',
    description='A simple utility to strip text after a semicolon',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

