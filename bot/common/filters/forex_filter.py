import telebot
from telebot.asyncio_filters import SimpleCustomFilter
from bot.common.db.users import get_existing_forex

class IsForexDB(SimpleCustomFilter):
    key='existing_forex'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await get_existing_forex(message.from_user.username): return True
        return False
