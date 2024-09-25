# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name='esymod',
            version='39.2024.9.25.9.10',
            packages=['esymod',],
            description='a python lib for project files',
            long_description='',
            author='Quanfa',
            package_data={
            '': ['*.*'],
            },
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            