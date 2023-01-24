from datetime import date
from bot import kaino, clientPayment
from bot.common.db.users import identifiership_update, membership_update, txn_link, cancel_link

payment_text = """
✎ Para realizar el pago del plan (por 100 dolares) puede usar los siguientes metodos.

✎ <a href="{URL_QR}">QRCODE.</a>
✎ <a href="{URL_CHECK}">Checkout.</a>

✎ <b>Una vez realizado el pago debe darle a /accepting recuerde este paso es muy IMPORTANTE para poder procesar su pago (Puede demorar unos 2m en que coinpayment lo de por OK, una vez que lo haga utilice el comando).</b>
"""

accepting_text = """
✎ <b> ¡El pago fue exitosamente realizado! </b>
"""

notAccepting_text = """
<b>
✎ Aun no has pagado, por favor, verifica bien el recibo de pago.

✎ En caso de tener problemas por favor,
✎ contactese al siguiente correo con una
✎ captura de su pago: support@kaino.io
</b>
"""

paymentTrue_text = """
> El usuario {} ya pago su membresia, (Recuerda estar atento para su cuenta de Deriv).
> Esta registro se realizo en la fecha: {}
> Trader: {}
> Invitado por: {}
"""

@kaino.message_handler(existing_user=True, check_txn=False, membership=False, commands=['membership'])
async def membership(message, data):
    user = data["user"]
    currency = "USDT.TRC20"
    payment = clientPayment.create_transaction(amount=100, currency1=currency, currency2=currency, buyer_email=user.email, buyer_name=user.fullname)
    txn = payment["result"]["txn_id"]
    await identifiership_update(message.from_user.username, txn)
    URL_QR=payment["result"]["qrcode_url"]
    URL_CHECK=payment["result"]["checkout_url"]
    await txn_link(message.from_user.username, URL_CHECK)
    await kaino.reply_to(message, payment_text.format(URL_QR=URL_QR, URL_CHECK=URL_CHECK), parse_mode="html", disable_web_page_preview=True)

@kaino.message_handler(existing_user=True, membership=False, commands=['cancel'])
async def cancel_link_membership(message):
    if await cancel_link(message.from_user.username):
       await kaino.reply_to(message, "🦉 El link ha sido eliminado con exito! Por favor, para generar uno nuevo utiliza; /membership")


@kaino.message_handler(existing_user=True, membership=False, commands=['accepting'])
async def accepting(message, data):
    user = data['membership']
    userInfo = data['user']
    username = message.from_user.username
    status = clientPayment.get_tx_info(txid=user.identifiership)["result"]["status"]
    if status >= 1:
         await membership_update(username, True)
         await kaino.send_message(617961155, paymentTrue_text.format(username, date.today()), userInfo.trader, userInfo.invite)
         await kaino.reply_to(message, accepting_text, parse_mode="html", disable_web_page_preview=True)
    else:
         await kaino.reply_to(message, notAccepting_text, parse_mode="html", disable_web_page_preview=True)
