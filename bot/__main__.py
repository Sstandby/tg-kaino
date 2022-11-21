#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging
import telebot
from bot import kaino
from bot.common import importdir
from bot.common.util.binance_check import BinanceClient, IsBinance
from telebot.async_telebot import asyncio_filters

# Enable logging
logging.getLogger('prisma').setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
logger = logging.getLogger(__name__)


importdir.do('bot/commands/auth', globals())
importdir.do('bot/commands/finance', globals())


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
kaino.add_custom_filter(IsBinance())
kaino.setup_middleware(BinanceClient())

if __name__ == "__main__":
    import asyncio
    asyncio.run(kaino.polling())
