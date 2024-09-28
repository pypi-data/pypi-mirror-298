from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Retrieve ESPN hidden api endpoints in a cleaned format'
LONG_DESCRIPTION = 'Retrieve ESPN hidden api endpoints in a cleaned format'

# Setting up
setup(
    name="espn_hidden_api",
    version=VERSION,
    author="peepei",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['espn_hidden_api'],
    install_requires=['pandas','requests'],
    keywords=['python', 'api','espn'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
