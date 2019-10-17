from setuptools import setup, find_packages

__name__ = 'tinypkg'
__author__ = 'Patrick Almhjell'
__email__ = 'palmhjell@caltech.edu'

__version__ = '0.0.1'


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description='A tiny, simple package for Recitation 3 of bebi103a (2019).',
    long_description=long_description,
    long_description_content_type='ext/markdown',
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)