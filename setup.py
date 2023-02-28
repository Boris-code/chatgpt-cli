# -*- coding: utf-8 -*-
"""
Created on 2022/8/4 11:38 上午
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""

from setuptools import setup, find_packages

setup(
    name="asst",
    version="1.3",
    packages=find_packages(),
    install_requires=["openai"],
    entry_points="""
        [console_scripts]
        asst=chatgpt.main:main
    """,
)
