import telebot
from telebot.asyncio_filters import SimpleCustomFilter
from bot.common.db.users import existing_user
from bot.common.db.payments import check_txn_link, membership

class IsUserDB(SimpleCustomFilter):
    key='existing_user'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await existing_user(message.from_user.username): return True
        return False

class CheckTxnLink(SimpleCustomFilter):
    key='check_txn'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await check_txn_link(message.from_user.username): return True
        return False

class IsMembership(SimpleCustomFilter):
    key='membership'
    @staticmethod
    async def check(message: telebot.types.Message):
        if await membership(message.from_user.username): return True
        return False
