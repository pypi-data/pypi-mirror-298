from setuptools import setup, find_packages
import os

VERSION = "0.0.1"
DESCRIPTION = "A library that makes it easy to make multiplayer"
LONG_DESCRIPTION = "A library that handles socketing backend, So you can focus on just your application."

# Setting up the library
setup(
    name = "multisocket",
    version = VERSION,
    author = "Kloodi",
    author_email = "<khaldbedoor@gmail.com>",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    keywords = ["python", "multiplayer", "server", "client", "networking", "host", "sockets"],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)