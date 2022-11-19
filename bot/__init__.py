import os
from pathlib import Path
from dotenv import load_dotenv
from telebot.asyncio_storage import StateMemoryStorage
from telebot.async_telebot import AsyncTeleBot

dotoenv_path = Path('../.env')
load_dotenv()

class Secrets():
    def __init__(self) -> None:
        self.token: str = os.getenv('token_tg')

secret = Secrets()
kaino = AsyncTeleBot(secret.token, state_storage=StateMemoryStorage())
