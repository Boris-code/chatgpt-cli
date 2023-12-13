# -*- coding: utf-8 -*-
"""
Created on 2022/12/8 8:55 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""
try:
    import readline
except Exception as e:
    pass

import os
import re
from os.path import dirname, join

import requests

from chatgpt.core import gpt

# from chatgpt.core import text_davinci_003


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Please conf OPENAI_API_KEY and set it to env")
    print("Example: export OPENAI_API_KEY=your key")
    print("详情见：https://github.com/Boris-code/chatgpt-cli")
    print("没有OPENAI_API_KEY，可加微信 boris_tm 获取")
    os._exit(0)


NEW_VERSION_TIP = """
──────────────────────────────────────────────────────
New version available \033[31m{version}\033[0m → \033[32m{new_version}\033[0m
Run \033[33mpip install --upgrade asst\033[0m to update!
"""

with open(join(dirname(__file__), "VERSION"), "rb") as f:
    VERSION = f.read().decode("ascii").strip()

# 修复window下print不能带颜色输出的问题
if os.name == "nt":
    os.system("")


def check_new_version():
    try:
        url = "https://pypi.org/simple/asst/"
        resp = requests.get(url, timeout=3)
        html = resp.text

        last_stable_version = re.findall(r"asst-([\d.]*?).tar.gz", html)[-1]
        now_version = VERSION
        now_stable_version = re.sub("-beta.*", "", VERSION)

        if now_stable_version < last_stable_version or (
            now_stable_version == last_stable_version and "beta" in now_version
        ):
            new_version = f"asst=={last_stable_version}"
            if new_version:
                version = f"asst=={VERSION.replace('-beta', 'b')}"
                tip = NEW_VERSION_TIP.format(version=version, new_version=new_version)
                print(tip)
    except Exception as e:
        pass


def main():
    gpt.run()
    check_new_version()


if __name__ == "__main__":
    main()
