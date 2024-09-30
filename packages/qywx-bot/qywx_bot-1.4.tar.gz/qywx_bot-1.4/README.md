## 介绍

作用：向企业微信群机器人发送信息

使用方式：

1. 新建 `.env`，写入企业微信 webhook key，例如：
    ```ini
    WEBHOOK_KEY = "asdf123456"
    ```
2. 发送信息
    ```Python
    from dotenv import load_dotenv
    load_dotenv()
    import os
    key = os.getenv("WEBHOOK_KEY")
    from qywx_bot.bot import Bot

    bot = Bot(key="...")
    bot.send_text(content="hello world")
    ```

## 环境

```
pip install requests
```