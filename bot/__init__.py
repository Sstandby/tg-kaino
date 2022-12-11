import os
from pathlib import Path
from dotenv import load_dotenv
from telebot.asyncio_storage import StateMemoryStorage
from telebot.async_telebot import AsyncTeleBot

dotoenv_path = Path('../.env')
load_dotenv()

class Secrets():
    def __init__(self) -> None:
        self.token = os.getenv('token_tg')
        self.kaino_pass = os.getenv('pass_db')

commands_IsBinance = ["hTrades", "hIncome", "balance", "positionInfo"]
commands_private = ["start", "token"]
secret = Secrets()
kaino_pass = secret.kaino_pass
kaino = AsyncTeleBot(secret.token, state_storage=StateMemoryStorage())
