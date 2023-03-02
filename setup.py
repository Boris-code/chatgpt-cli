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

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    version="1.6",
    name="asst",
    license="MIT",
    author="Boris",
    author_email="boris_liu@foxmail.com",
    packages=find_packages(),
    install_requires=["openai"],
    entry_points="""
        [console_scripts]
        asst=chatgpt.main:main
    """,
    description="ChatGPT shell command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Boris-code/chatgpt-cli.git",
    classifiers=["Programming Language :: Python :: 3"],
)
