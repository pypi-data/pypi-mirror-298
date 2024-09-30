from qywx_bot.bot import Bot
from dotenv import load_dotenv
load_dotenv()
import os
key = os.getenv("WEBHOOK_KEY")

qybot = Bot(key)
qybot.send_text