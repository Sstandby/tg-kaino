import telebot
from telebot.asyncio_filters import SimpleCustomFilter
from bot.common.db.users import get_forex_existing

class IsForexDB(SimpleCustomFilter):
    key='existing_forex'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await get_forex_existing(message.from_user.username): return True
        return False
