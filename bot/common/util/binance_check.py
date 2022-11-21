import telebot
from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
from bot.common.db.users import existing_user, get_api_key, get_api_secret
from telebot.custom_filters import SimpleCustomFilter
from telebot.handler_backends import BaseMiddleware

class BinanceClient(BaseMiddleware):
    def __init__(self):
        self.update_types = ['message']
    async def pre_process(self, message, data):
        api_key = await get_api_key(message.from_user.username)
        api_secret = await get_api_secret(message.from_user.username)
        data['client'] = await AsyncClient.create(api_key, api_secret)

    async def post_process(self, message, data, exception=None):
        if exception:
            print(exception)

class IsBinance(SimpleCustomFilter):
    key='binance_user'
    @staticmethod
    def check(message: telebot.types.Message):
        if existing_user(message.from_user.username): return True
