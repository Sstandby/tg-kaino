from bot import commands_IsMembership, commands_GetInfo
from bot.common.db.users import get_user_info, get_membership_info
from telebot.handler_backends import BaseMiddleware

class UserDBMiddlware(BaseMiddleware):

    def __init__(self):
        self.update_types = ['message']

    async def pre_process(self, message, data):
        if message.text[1:] in commands_IsMembership:
            user = await get_user_info(message.from_user.username)
            data['user'] = user
        if message.text[1:] in commands_GetInfo:
            membership = await get_membership_info(message.from_user.username)
            data['membership'] = membership
    async def post_process(self, message, data, exception=None):
        if exception:
            print(exception)
