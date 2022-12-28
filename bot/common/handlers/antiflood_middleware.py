from bot import kaino
from telebot.handler_backends import BaseMiddleware, CancelUpdate

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']
        # Always specify update types, otherwise middlewares won't work

    async def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:
            # User is not in a dict, so lets add and cancel this function
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            # User is flooding
            await kaino.send_message(message.chat.id, 'Haz realizado muchas solicitudes, ve con calma!')
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date


    async def post_process(self, message, data, exception):
        pass
