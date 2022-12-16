from bot import kaino, clientPayment
from bot.common.db.users import identifiership_update, membership_update

payment_text = """
✎ Para realizar el pago del plan (por 100 dolares) puede usar los siguientes metodos.

✎ <a href="{URL_QR}">QRCODE.</a>
✎ <a href="{URL_CHECK}">Checkout.</a>

✎ <b>Una vez realizado el pago debe darle a /accepting recuerde este paso es muy IMPORTANTE para poder procesar su pago.</b>
"""

accepting_text = """
✎ <b> ¡El pago fue exitosamente realizado! </b>
"""

notAccepting_text = """
<b>
✎ Aun no has pagado, por favor, verifica bien el recibo de pago.

✎ En caso de tener problemas por favor,
✎ contactese al siguiente correo con una
✎ captura de su pago: support@kaino.com
</b>
"""

@kaino.message_handler(existing_user=True, commands=['membership'])
async def membership(message, data):
    user = data["user"]
    currency = "USDT.TRC20"
    payment = clientPayment.create_transaction(amount=100, currency1=currency, currency2=currency, buyer_email=user.email, buyer_name=user.fullname)
    txn = payment["result"]["txn_id"]
    await identifiership_update(message.from_user.username, txn)
    URL_QR=payment["result"]["qrcode_url"]
    URL_CHECK=payment["result"]["checkout_url"]
    await kaino.reply_to(message, payment_text.format(URL_QR=URL_QR, URL_CHECK=URL_CHECK), parse_mode="html", disable_web_page_preview=True)

@kaino.message_handler(existing_user=True, commands=['accepting'])
async def accepting(message, data):
    user = data["user"]
    status = clientPayment.get_tx_info(txid=user.identifiership)["result"]["status"]
    if status >= 1:
         await membership_update(message.from_user.username, True)
         await kaino.reply_to(message, accepting_text, parse_mode="html", disable_web_page_preview=True)
    else:
         await kaino.reply_to(message, notAccepting_text, parse_mode="html", disable_web_page_preview=True)
