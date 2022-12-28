#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging
from bot import kaino
from bot.common import importdir
from telebot.async_telebot import asyncio_filters
from bot.common.filters.admin_filter import IsAdmin
from bot.common.filters.user_filter import IsUserDB, IsMembership
from bot.common.handlers.user_middleware import UserDBMiddlware
from bot.common.handlers.binance_middleware import BinanceClientMiddleware
from bot.common.handlers.antiflood_middleware import AntiFloodMiddleware
# Enable logging
#logging.getLogger('prisma').setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
logger = logging.getLogger(__name__)


importdir.do('bot/commands/auth', globals())
importdir.do('bot/commands/finance/futures', globals())
importdir.do('bot/commands/finance/coinpayments', globals())
importdir.do('bot/commands/admin', globals())
importdir.do('bot/common/exceptions', globals())


start_text = """
╔══════════════════════╗
    ¡✩ Aqui kaino presentandose ✩!
   ❝ Recuerde seleccionar la opción
            que mas se ajusta a sus
                     necesidades. ❞
╚══════════════════════╝
"""

@kaino.message_handler(commands=['start'])
async def start(message):
    await kaino.reply_to(message, start_text)

kaino.add_custom_filter(asyncio_filters.StateFilter(kaino))
kaino.add_custom_filter(asyncio_filters.IsDigitFilter())
kaino.add_custom_filter(IsAdmin())
kaino.add_custom_filter(IsUserDB())
kaino.add_custom_filter(IsMembership())
kaino.setup_middleware(BinanceClientMiddleware())
kaino.setup_middleware(UserDBMiddlware())
kaino.setup_middleware(AntiFloodMiddleware(3))

if __name__ == "__main__":
    import asyncio
    asyncio.run(kaino.polling())
