# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name = "pyNTCIREVAL",
    packages = ["pyNTCIREVAL", "pyNTCIREVAL.metrics"],
    version = "0.0.3",
    description = "Python version of NTCIREVAL",
    author = "Makoto P. Kato",
    author_email = "mpkato@slis.tsukuba.ac.jp",
    license     = "MIT License",
    url = "https://github.com/mpkato/pyNTCIREVAL",
    entry_points='''
        [console_scripts]
        pyNTCIREVAL=pyNTCIREVAL.main:cli
    ''',
    install_requires = [
        'numpy',
        'click'
    ],
    tests_require=['pytest'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['information retrieval', 'evaluation']
)
