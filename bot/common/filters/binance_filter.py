import telebot
from telebot.asyncio_filters import SimpleCustomFilter
from bot.common.db.users import existing_user
from binance.exceptions import BinanceAPIException

class IsBinance(SimpleCustomFilter):
    key='binance_user'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await existing_user(message.from_user.username): return True
        return False
