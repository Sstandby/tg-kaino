from bot import kaino
import json
from binance.exceptions import BinanceAPIException

@kaino.message_handler(binance_user=True, commands=['hTrades'])
async def history_trades(message, data: dict):
    """
    Get older market historical trades
    """
    try:
        client = data['client']
        trades = await client.futures_coin_historical_trades(symbol='BTCUSD_PERP')
        print(json.dumps(trades, indent=2))
        await kaino.reply_to(message, f"{json.dumps(trades, indent=2)}")
    except BinanceAPIException as e:
        await kaino.reply_to(message, f"Error: {e}")
