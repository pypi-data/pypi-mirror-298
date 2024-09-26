# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from varjson import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="varjson",
    packages=find_packages(exclude=["tests"]),
    version=__version__,
    url="https://github.com/MLuehr/EnvJSON",
    license="MIT",
    author="Mathias",
    description="Simple JSON configuration file parser with easy access for structured data",
    install_requires=[],
    python_requires=">=3.9",
    include_package_data=True,
    platforms="any",
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
