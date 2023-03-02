# -*- coding: utf-8 -*-
"""
Created on 2022/12/8 8:55 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""

import os
import readline

from core import gpt_35_turbo


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Please conf OPENAI_API_KEY and set it to env")
    print("Example: export OPENAI_API_KEY=your key")
    os._exit(0)


def main():
    gpt_35_turbo.main()


if __name__ == "__main__":
    main()
