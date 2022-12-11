from bot import kaino
from telebot.handler_backends import BaseMiddleware
from binance.exceptions import BinanceAPIException

@kaino.message_handler(isBinance=True, commands=['positionInfo'])
async def balance(message, data: dict):
    """
    Get position information
    """
    try:
        client = data['client']
        position = await client.futures_coin_position_information()
        await kaino.reply_to(message, f"{position}")
    except BinanceAPIException as e:
        await kaino.reply_to(message, f"Error: {e}")
