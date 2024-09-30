import requests

from . import check

class Bot():
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
    header = {"Content-Type": "application/json"}
    def __init__(self, key: str) -> None:
        self.key = key
        self.url = Bot.url
        self.header = Bot.header
    
    def send_text(self, content: str):
        """发送text

        Args:
            content (str): 文本内容，最长不超过2048个字节，必须是utf8编码
        """
        check.text(content)
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        requests.post(f"{self.url}{self.key}", json=data, headers=self.header)

        #todo: mentioned_list, mentioned_mobile_list
    
