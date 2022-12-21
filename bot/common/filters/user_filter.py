import telebot
from telebot.asyncio_filters import SimpleCustomFilter
from bot.common.db.users import existing_user, membership
from binance.exceptions import BinanceAPIException

class IsUserDB(SimpleCustomFilter):
    key='existing_user'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await existing_user(message.from_user.username): return True
        return False

class IsMembership(SimpleCustomFilter):
    key='membership'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await membership(message.from_user.username): return True
        return False
