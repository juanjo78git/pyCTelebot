# -*- coding: utf-8 -*-


from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from pyCTelebot.config.auth import TOKEN_TELEGRAM, WEBHOOK_URL_TELEGRAM, PORT, USER_ADMIN
from pyCTelebot import pyCrypto
import gettext
import logging

# i18n
_ = gettext.gettext
# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def run(how):
    # Conexion
    updater = Updater(token=TOKEN_TELEGRAM, use_context=True)
    dispatcher = updater.dispatcher

    # Eventos que activarán nuestro bot.
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)

    help_handler = CommandHandler('help', help_command)
    dispatcher.add_handler(help_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    price_handler = CommandHandler('price', price)
    dispatcher.add_handler(price_handler)

    open_orders_handler = CommandHandler('orders', open_orders)
    dispatcher.add_handler(open_orders_handler)

    buy_handler = CommandHandler('buy', buy)
    dispatcher.add_handler(buy_handler)

    buy_limit_handler = CommandHandler('buylimit', buy_limit)
    dispatcher.add_handler(buy_limit_handler)

    sell_handler = CommandHandler('sell', sell)
    dispatcher.add_handler(sell_handler)

    cancel_order_handler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancel_order_handler)

    # Ultimo evento para comandos desconocidos.
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Controlador de errores
    dispatcher.add_error_handler(error_callback)

    # Comienza el bot
    if how == 'w':
        # O se arranca con webhook
        logger.log(msg='Start with webhook', level=logging.INFO)
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN_TELEGRAM,
                              webhook_url=WEBHOOK_URL_TELEGRAM + TOKEN_TELEGRAM)
    else:
        # O se arranca con polling
        logger.log(msg='Start with polling', level=logging.INFO)
        updater.start_polling()

    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()


def start(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='start'):
        return 1
    if len(update.effective_message.text.split(' ', 1)) == 2:
        symbol = update.effective_message.text.split(' ', 1)[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        context.user_data["symbol"] = symbol
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Selected trading pair: {0}").format(symbol))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Hello!"))


def stop(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='stop'):
        return 1
    context.user_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("Bye!!"))


# Eco de lo que digas
def echo(update: Update, context: CallbackContext):
    # if not authorization(update=update, context=context, action='echo'):
    #    return 1
    # context.bot.send_message(chat_id=update.effective_chat.id, text=_("{0} said: {1}").format(
    #    update.effective_user.first_name, update.message.text))
    return 1


def help_command(update: Update, context: CallbackContext):
    """
    @BotFather /setcommands
    start - Select a trading pair to work
    stop - Clean all
    price - Current trading pair price
    orders - Show all open orders for the trading pair
    buy - Send a new purchase order
    buylimit - Send a new limit purchase order
    sell - Send a new sales order
    selllimit - Send a new limit sales order
    cancel - Cancel open order
    help - This help
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("You can control me by sending these commands: \n"
                                    "\n"
                                    "/start [SYMBOL] - Select a trading pair to work \n"
                                    "/stop - Clean all \n"
                                    "/price [SYMBOL] - Current trading pair price \n"
                                    "/orders [SYMBOL] - Show all open orders for the trading pair \n"
                                    "/buy [SYMBOL] [AMOUNT] - Send a new purchase order \n"
                                    "/buylimit [SYMBOL] [AMOUNT] [PRICE] - Send a new limit purchase order \n"
                                    "/sell [SYMBOL] [AMOUNT] - Send a new sales order \n"
                                    "/selllimit [SYMBOL] [AMOUNT] [PRICE] - Send a new limit sales order \n"
                                    "/cancel [SYMBOL] [ORDER ID] - Cancel open order \n"
                                    "/help  - This help"))


def price(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='price'):
        return 1
    if len(update.effective_message.text.split(' ', 1)) == 2:
        symbol = update.effective_message.text.split(' ', 1)[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(update.effective_message.text.split(' ', 1)) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]

    if 'symbol' in locals():
        logger.log(msg='/price symbol used: {0}'.format(symbol), level=logging.INFO)
        last_price = pyCrypto.price(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} Last price: {1}").format(
                                     symbol,
                                     last_price))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def open_orders(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='open_orders'):
        return 1
    if len(update.effective_message.text.split(' ', 1)) == 2:
        symbol = update.effective_message.text.split(' ', 1)[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(update.effective_message.text.split(' ', 1)) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]

    if 'symbol' in locals():
        logger.log(msg='/orders symbol used: {0}'.format(symbol), level=logging.INFO)
        orders = pyCrypto.open_orders(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} orders: {1}").format(
                                     symbol,
                                     orders))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def buy(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='buy'):
        return 1
    logger.log(msg='/buy', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 3:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = update.effective_message.text.split(' ')[2]
    elif len(update.effective_message.text.split(' ')) == 2 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = update.effective_message.text.split(' ')[1]
    if 'symbol' in locals() and 'amount' in locals():
        logger.log(msg='/buy symbol: {0}, amount: {1}'.format(symbol, amount), level=logging.INFO)
        status = pyCrypto.buy_order(symbol=symbol, amount=amount, type_order='market')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Buying order with symbol {0} and amount {1} --> status {2}").format(
                                     symbol,
                                     amount,
                                     status))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def buy_limit(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='buylimit'):
        return 1
    logger.log(msg='/buylimit', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 4:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = update.effective_message.text.split(' ')[2]
        price = update.effective_message.text.split(' ')[3]
    elif len(update.effective_message.text.split(' ')) == 3 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = update.effective_message.text.split(' ')[1]
        price = update.effective_message.text.split(' ')[2]
    if 'symbol' in locals() and 'amount' in locals() and 'price' in locals():
        logger.log(msg='/buylimit symbol: {0}, amount: {1}, price: {2}'.format(symbol, amount, price), level=logging.INFO)
        status = pyCrypto.buy_order(symbol=symbol, amount=amount, type_order='limit', price=price)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Create limit buy order with symbol {0}, amount {1} and  price {2}--> status {3}").format(
                                     symbol,
                                     amount,
                                     price,
                                     status))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def sell(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='sell'):
        return 1
    logger.log(msg='/sell', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 3:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = update.effective_message.text.split(' ')[2]
    elif len(update.effective_message.text.split(' ')) == 2 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = update.effective_message.text.split(' ')[1]
    if 'symbol' in locals() and 'amount' in locals():
        logger.log(msg='/sell symbol: {0}, amount: {1}'.format(symbol, amount), level=logging.INFO)
        status = pyCrypto.sell_order(symbol=symbol, amount=amount, type_order='market')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Selling order with symbol {0} and amount {1} --> status {2}").format(
                                     symbol,
                                     amount,
                                     status))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def sell_limit(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='selllimit'):
        return 1
    logger.log(msg='/selllimit', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 4:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = update.effective_message.text.split(' ')[2]
        price = update.effective_message.text.split(' ')[3]
    elif len(update.effective_message.text.split(' ')) == 3 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = update.effective_message.text.split(' ')[1]
        price = update.effective_message.text.split(' ')[2]
    if 'symbol' in locals() and 'amount' in locals() and 'price' in locals():
        logger.log(msg='/selllimit symbol: {0}, amount: {1}, price: {2}'.format(symbol, amount, price),
                   level=logging.INFO)
        status = pyCrypto.sell_order(symbol=symbol, amount=amount, type_order='limit', price=price)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Create limit sell order with symbol {0}, amount {1} and  price {2}--> status {3}").format(
                                     symbol,
                                     amount,
                                     price,
                                     status))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def cancel(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='cancel'):
        return 1
    logger.log(msg='/cancel', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 3:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        orderid = update.effective_message.text.split(' ')[2]
    elif len(update.effective_message.text.split(' ')) == 2 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        orderid = update.effective_message.text.split(' ')[1]
    if 'symbol' in locals() and 'orderid' in locals():
        logger.log(msg='/cancel symbol: {0}, orderid: {1}'.format(symbol, orderid), level=logging.INFO)
        status = pyCrypto.cancel_order(orderid=orderid, symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Canceling order with symbol {0} and id {1} --> status {2}").format(
                                     symbol,
                                     orderid,
                                     status))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("Sorry, I didn't understand that command."))


def authorization(update: Update, context: CallbackContext, action):
    logger.log(msg='User: {0} action: {1}'.format(update.effective_user.id, action), level=logging.INFO)
    if str(update.effective_user.id) in USER_ADMIN:
        return True
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return False
