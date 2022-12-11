import calendar, time, json
from bot import kaino
from telebot.handler_backends import BaseMiddleware
from binance.exceptions import BinanceAPIException

@kaino.message_handler(commands=['hIncome'])
async def income(message, data: dict):
    """
    Get income history for authenticated account
    """
    try:
        client = data['client']
        timestamp = await client.get_server_time()
        income = await client.futures_coin_income_history(timestamp=timestamp)
        print(json.dumps(income, indent=2))
        await kaino.reply_to(message, f"{json.dumps(income, indent=2)}")
    except BinanceAPIException as e:
        await kaino.reply_to(message, f"Error: {e}")
