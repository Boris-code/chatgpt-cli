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
from typing import (
    Iterator,
    Optional,
)

import requests

api_key = os.getenv("OPENAI_API_KEY")


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
        "Authorization": "Bearer {}".format(api_key),
    }
    url = "https://api.openai.com/v1/chat/completions"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.2,
        "stream": True,
        "user": api_key,
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
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

                print(message, end="")
                answer += message

            messages.append({"role": "assistant", "content": answer})
            if len(str(messages)) > 2048:
                messages = messages[-3:]
            print("\n\n")

        except (KeyboardInterrupt, EOFError) as e:
            print("\nBye~")
            break

        except Exception as e:
            print("Exception: ", e)
            retry = input("Sorry, I have an exception. Try again（Y/N）").lower()


if __name__ == "__main__":
    main()
