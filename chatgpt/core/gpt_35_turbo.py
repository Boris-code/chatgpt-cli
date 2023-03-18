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

import requests
import urllib3

# 忽略 InsecureRequestWarning 报警信息
warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)


API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1/chat/completions")
PROXY = os.getenv("ASST_PROXY")


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
        "Authorization": "Bearer {}".format(API_KEY),
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.2,
        "stream": True,
        "user": API_KEY,
    }
    response = requests.post(
        OPENAI_URL,
        headers=headers,
        json=data,
        stream=True,
        timeout=30,
        proxies={"https": PROXY} if PROXY else None,
        verify=False,
    )
    if response.status_code != 200:
        raise Exception(response.text)

    for line in parse_stream(response.iter_lines()):
        data = json.loads(line)
        yield data["choices"]


def main():
    messages = []
    retry = False

    while True:
        try:
            try:
                if retry != "y":
                    question = input("You: ")
                    messages.append({"role": "user", "content": question})

                retry = False

                resp = request(messages)

                is_content = False
                answer = ""
                for data in resp:
                    message = data[0]["delta"].get("content", "")
                    if not is_content:
                        if message.strip() == "":
                            continue
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
                if not PROXY:
                    print(
                        "\033[31mConnectTimeout: {}\033[0m".format(
                            "请求超时，如为国内用户请设置境外代理，设置方式见：https://github.com/Boris-code/chatgpt-cli"
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
    main()
