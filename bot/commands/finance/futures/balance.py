import json
from bot import kaino
from telebot.handler_backends import BaseMiddleware
from binance.exceptions import BinanceAPIException

@kaino.message_handler(commands=['balance'])
async def balance(message, data: dict):
    try:
        client = data['client']
        timestamp = await client._get_earliest_valid_timestamp('BTCUSDT', '1d')
        print(timestamp)
        balance = await client.futures_coin_account_balance(timestamp=timestamp)
        await kaino.reply_to(message, f"{balance}")
    except BinanceAPIException as e:
        await kaino.reply_to(message, f"Error: {e}")
