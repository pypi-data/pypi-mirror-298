# coding: UTF-8
# Copyright © 2024 HuyKaiser. All rights reserved.

from setuptools import setup


setup(
    name='gencardhks',
    description='A simple class for identifying, validating, and formatting credit card',
    version='1.0.3',
    author='HuyKaiser',
    author_email='nguyenhuy34789@gmail.com',
    maintainer='huykaiser',
    maintainer_email='nguyenhuy34789@gmail.com',
    url='https://github.com/huykaiserOwO/creditcard',
    packages=[
        'huykaiser',
    ],
    package_dir={
        'huykaiser': './huykaiser',
    },
    package_data={
        'huykaiser': [
            './data/registry.xml',
        ],
    }
)
