'''
encoding:   -*- coding: utf-8 -*-
@Time           :  2024/9/25 12:20
@Project_Name   :  SendEmail
@Author         :  lhw
@File_Name      :  setup.py.py

功能描述

实现步骤

'''
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setup(
    name='lhw-send-email',
    version='0.0.2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='骆鸿威',
    author_email='1959415641@qq.com',
    url='https://github.com/Th5200/SendEmail',
    license='MIT',
    install_requires=[],
    python_requires=">=3.7, <=3.12",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
)