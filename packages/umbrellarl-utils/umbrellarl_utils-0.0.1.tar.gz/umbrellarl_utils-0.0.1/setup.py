"""PyPi config."""

from setuptools import setup, find_packages

setup(
    name='umbrellarl_utils',
    version='0.0.1',
    packages=find_packages(),
    description='Utilities for UmbrellaRL modules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Christopher Torrington',
    author_email='ctorrington1@gmail.com',
    url='https://github.com/UmbrellaRL/utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.12'
)
