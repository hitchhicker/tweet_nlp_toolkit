import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'tweet_nlp_toolkit', '__version__.py'), 'r') as f:
    exec(f.read(), about)
setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    classifiers=(
        "Programming Language :: Python :: 3.6"
    ),
    install_requires=[
        "anyascii==0.3.0",
        "certifi==2021.5.30",
        "charset-normalizer==2.0.12",
        "contractions==0.0.25",
        "docopt==0.6.2",
        "emoji==1.6.3",
        "idna==3.3",
        "jieba==0.42.1",
        "mecab-python3==0.996.5",
        "mosestokenizer==1.2.1",
        "openfile==0.0.7",
        "pyahocorasick==1.4.4",
        "pycld2==0.41",
        "pythainlp==2.3.2",
        "python-crfsuite==0.9.7",
        "requests==2.27.1",
        "textsearch==0.0.21",
        "tinydb==4.7.0",
        "toolwrapper==2.1.0",
        "typing_extensions==4.1.1",
        "uctools==1.3.0",
        "urllib3==1.26.8"
    ]
)
