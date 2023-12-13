# ChatGPT-CLI
> ChatGPT shell command
> Support gpt-4

ChatGPT 支持终端命令行啦，支持gpt-4

支持连续对话，在终端输入asst即可开启对话。

如让它写个feapder的爬虫，实际对答如下：

![](media/16788027988798.jpg)

## 安装

```shell
pip install asst
```

## 环境变量

| 变量 | 必须 | 描述                                                                                                        |
| ----|--|-----------------------------------------------------------------------------------------------------------|
| OPENAI_API_KEY| 是 | OpenAI的密钥                                                                                                 |
| OPENAI_BASE_URL |否 | OpenAI的镜像接口地址，如：https://api.openai.com， 注意不需要携带 v1/chat/completions |
| OPENAI_PROXY| 否 | 代理，如 username:password@ip:port                                                                            |
| OPENAI_MODEL| 否 |模型， 支持 gpt-4-1106-preview、gpt-3.5-turbo等，默认为 gpt-4-1106-preview |


## 配置

> 没有OPENAI_API_KEY，openai官网自己搞

设置`OPENAI_API_KEY="chatgpt的密钥"`到环境变量

**mac或linux下**
临时设置的方式
```
export OPENAI_API_KEY=your key
```
永久设置
```
vim ~/.bash_profile

# 在合适的位置添加环境变量
export OPENAI_API_KEY="your key"
```

**window下设置为系统环境变量**

参考：<a href="https://blog.csdn.net/xue_nuo/article/details/114793534" target="_blank">https://blog.csdn.net/xue_nuo/article/details/114793534</a>

## 使用

```shell
> asst
You: hello
Bot: Hi there!
```

## 请求超时

国内用户因为墙的原因，无法直接访问chatgpt，需配置镜像api或使用代理

代理使用方式：

设置`ASST_PROXY="代理"`到环境变量

如：

```
export ASST_PROXY="username:password@ip:port"
```

## 境外代理举例

**推荐：brightdata**

不需要公司、不需要实名，准备好邮箱即可

地址：<a href="https://brightdata.grsm.io/r0g6zla8seqs" target="_blank">https://brightdata.grsm.io/r0g6zla8seqs</a>

若提示认证，选择支付宝即可，并不需要真正的认证

充值支持支付宝

使用方式：

1. 选择机房代理，因为便宜。追求稳定选择住宅

    ![](media/16788015593888.jpg)
    
2. 配置：

    ![](media/16788016828506.jpg)
    
3. 查看访问参数

![](media/16788017441719.jpg)

4. 配置代理

    设置`ASST_PROXY="代理"`到环境变量
    
    如：
    
    ```
    export ASST_PROXY="用户名:密码@主机"
    ```

## OPENAI_API_KEY

在chatgpt官网申请



