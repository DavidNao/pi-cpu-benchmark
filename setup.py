# https://packaging.python.org/en/latest/tutorials/packaging-projects/
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    'plotext==4.1.3',
    'psutil==5.8.0'
]

setup(
    name='SuperPi',
    version='1.0',
    description='A simple CPU benchmark',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='David Steinmetz',
    packages=['superpi'],
    install_requires=requirements
)
