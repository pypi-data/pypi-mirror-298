from setuptools import setup, find_packages

VERSION = "1.2"
DESCRIPTION = "A library that makes it easy to make multiplayer"
LONG_DESCRIPTION = ""

with open("README.md", "r") as file:
    LONG_DESCRIPTION = file.read()

# Setting up the library
setup(
    name = "multisocketing",
    version = VERSION,
    author = "ticks",
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