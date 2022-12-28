import telebot
from telebot.asyncio_filters import SimpleCustomFilter

class IsAdmin(SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    async def check(message: telebot.types.Message):
        if message.from_user.username in ['Standbii', 'KainoDLR']: return True
        return False
