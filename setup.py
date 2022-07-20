import os

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
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
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6"
    ],
    install_requires=[
        "pycld2==0.41",
        "mecab-python3==0.996.5",
        "contractions==0.0.25",
        "emoji==1.6.3",
        "mosestokenizer==1.2.1",
        "jieba==0.42.1",
        "pythainlp==2.3.2",
    ]
)
