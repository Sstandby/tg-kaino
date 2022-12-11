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
        await kaino.reply_to(message, f"{json.dumps(trades, indent=2)}")
    except BinanceAPIException as e:
        if e.status_code == 401:
            await kaino.reply_to(message, f"✎ La API KEY no es valida, cambia la API que has puesto por otra con /token.")
