from bot import kaino
from bot import commands_GetInfoMembership, commands_all
from bot.common.db.users import get_user_info, get_membership_info
from telebot.handler_backends import BaseMiddleware
from telebot.asyncio_handler_backends import State

class UserDBMiddlware(BaseMiddleware):

    def __init__(self):
        self.update_types = ['message']

    async def pre_process(self, message, data):
        if message.text[1:] in ["membership", "forex",  "forexPayment", "acceptingForex" , "accepting"]:
            user = await get_user_info(message.from_user.username)
            data['user'] = user
        if message.text[1:] in commands_GetInfoMembership:
            membership = await get_membership_info(message.from_user.username)
            data['membership'] = membership
    async def post_process(self, message, data, exception=None):
        if exception:
            print(exception)

class StateDeleteMiddlware(BaseMiddleware):

    def __init__(self):
        self.update_types = ['message']

    async def pre_process(self, message, data):
        if message.text[1:] in commands_all:
          await kaino.delete_state(message.from_user.id, message.chat.id)
    async def post_process(self, message, data, exception=None):
        if exception:
            print(exception)
