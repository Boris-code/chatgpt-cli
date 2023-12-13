# -*- coding: utf-8 -*-
"""
Created on 2023/3/2 16:43
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""
import json
import os
import warnings
from typing import (
    Iterator,
    Optional,
)
from urllib.parse import urljoin

import requests
import urllib3

# 忽略 InsecureRequestWarning 报警信息
warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com")
OPENAI_PROXY = os.getenv("OPENAI_PROXY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")


def parse_stream_helper(line: bytes) -> Optional[str]:
    if line:
        if line.strip() == b"data: [DONE]":
            # return here will cause GeneratorExit exception in urllib3
            # and it will close http connection with TCP Reset
            return None
        if line.startswith(b"data: "):
            line = line[len(b"data: ") :]
            return line.decode("utf-8")
        else:
            return None
    return None


def parse_stream(rbody: Iterator[bytes]) -> Iterator[str]:
    for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line


def request(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(OPENAI_API_KEY),
    }
    data = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "stream": True,
        "user": OPENAI_API_KEY,
    }
    response = requests.post(
        urljoin(OPENAI_BASE_URL, "/v1/chat/completions"),
        headers=headers,
        json=data,
        stream=True,
        timeout=30,
        proxies={"https": OPENAI_PROXY} if OPENAI_PROXY else None,
        verify=False,
    )
    if response.status_code != 200:
        raise Exception(response.text)

    for line in parse_stream(response.iter_lines()):
        data = json.loads(line)
        yield data["choices"]


def run():
    messages = []
    retry = False

    tip = """

 █████╗ ███████╗███████╗████████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝
███████║███████╗███████╗   ██║   
██╔══██║╚════██║╚════██║   ██║   
██║  ██║███████║███████║   ██║   
╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   

ASST智能助手，支持chatgpt-4，支持多行输入                             
    """
    print(tip)

    while True:
        try:
            try:
                if retry != "y":
                    print("请输入问题，\033[33m回车 + 空格 + 回车\033[0m 发送消息:")
                    question = []
                    stopword = " "  # 停止条件
                    for line in iter(
                        input, stopword
                    ):  # iter()中第一个参数是可调用的，即可以像函数一样调用他，因此是input，而不是input（）
                        question.append(line)

                    question = "\n".join(question)
                    messages.append({"role": "user", "content": question})

                print("\n我已收到你的问题，正在思考中...", end="", flush=True)

                retry = False

                resp = request(messages)

                is_content = False
                answer = ""
                for data in resp:
                    message = data[0]["delta"].get("content", "")
                    if not is_content:
                        if message.strip() == "":
                            continue
                        print("\r" + " " * 50 + "\r", end="")  # 先清空当前行
                        is_content = True

                    print("\033[32m" + message + "\033[0m", end="")
                    answer += message

                messages.append({"role": "assistant", "content": answer})
                if len(str(messages)) > 2048:
                    messages = messages[-3:]
                print("\n\n")

            except (KeyboardInterrupt, EOFError) as e:
                print("\nBye~")
                break

            except requests.exceptions.ConnectTimeout as e:
                if not OPENAI_PROXY:
                    print(
                        "\033[31mConnectTimeout: {}\033[0m".format(
                            "请求超时，如为国内用户可设置API镜像地址或使用境外代理，设置方式见：https://github.com/Boris-code/chatgpt-cli"
                        )
                    )
                    print("\nBye~")
                    break
                else:
                    print("\033[31mConnectTimeout: {}\033[0m".format(e))
                    retry = input("Sorry, I have an exception. Try again:（Y/N）").lower()

            except Exception as e:
                print("\033[31mException: {}\033[0m".format(e))
                retry = input("Sorry, I have an exception. Try again:（Y/N）").lower()

        except (KeyboardInterrupt, EOFError) as e:
            print("\nBye~")
            break


if __name__ == "__main__":
    run()
