# -*- coding: utf-8 -*-
"""
Created on 2023/3/2 16:43
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""


import os

import openai

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def main():
    prompt = ""
    retry = False

    while True:
        try:
            if retry != "y":
                question = input("You: ")
                prompt += "User: {}\n".format(question)

            # print(prompt)
            retry = False

            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,  # 必填参数，指定输入的文本，可以是一句话或一个段落。
                temperature=0.5,  # 可选参数，控制生成文本的多样性，值越高则生成的文本越不可预测。默认值为 0.5
                stream=True,  # 流式返回
                max_tokens=2048,  # 限制生成的文本的最大长度
                top_p=1,  # 用来控制生成文本的质量。数值越高，生成的文本质量就越高。
                n=1,  # 可选参数，指定要生成的文本数量。默认值为 1
                frequency_penalty=0.0,  # 控制生成文本中重复单词的频率。数值越高，重复单词的频率就越低。
                presence_penalty=0.0,  # 控制生成文本中常见单词的频率。数值越高，常见单词的频率就越低。
                user="Boris",  # 可选参数，用于向 GPT 模型提供用户信息，例如用户 ID、用户名等
            )

            is_content = False
            answer = ""
            for data in resp:
                text = data.get("choices")[0].get("text")
                if not is_content:
                    if text.strip() == "":
                        continue
                    is_content = True

                print(text, end="")
                answer += text

            prompt += answer + "\n"
            if len(prompt) > 2048:
                prompt = prompt[-2048:]
            print("\n\n")

        except (KeyboardInterrupt, EOFError) as e:
            print("\nBye~")
            break

        except Exception as e:
            print("Exception: ", e)
            retry = input("Sorry, I have an exception. Try again（Y/N）").lower()


if __name__ == "__main__":
    main()
