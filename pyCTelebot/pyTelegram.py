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

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    price_handler = CommandHandler('price', price)
    dispatcher.add_handler(price_handler)

    openorders_handler = CommandHandler('orders', openorders)
    dispatcher.add_handler(openorders_handler)

    buy_handler = CommandHandler('buy', buy)
    dispatcher.add_handler(buy_handler)

    sell_handler = CommandHandler('sell', sell)
    dispatcher.add_handler(sell_handler)

    cancelorder_handler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancelorder_handler)

    # Ultimo evento para comandos desconocidos.
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Controlador de errores
    dispatcher.add_error_handler(error_callback)

    # Comienza el bot
    print('Hello Bot!')

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


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("You can control me by sending these commands: \n"
                                    "\n"
                                    "/start [SYMBOL] - Select a trading pair to work \n"
                                    "/stop - Clean all \n"
                                    "/price [SYMBOL] - Current trading pair price \n"
                                    "/orders [SYMBOL] - Show all open orders for the trading pair \n"
                                    "/buy [PARAMS] - Send a new purchase order \n"
                                    "/sell [PARAMS] - Send a new sales order \n"
                                    "/cancel [PARAMS] - Cancel open order \n"
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
        lastprice = pyCrypto.price(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} Last price: {1}").format(
                                     symbol,
                                     lastprice))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def openorders(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='openorders'):
        return 1
    if len(update.effective_message.text.split(' ', 1)) == 2:
        symbol = update.effective_message.text.split(' ', 1)[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(update.effective_message.text.split(' ', 1)) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]

    if 'symbol' in locals():
        logger.log(msg='/orders symbol used: {0}'.format(symbol), level=logging.INFO)
        orders = pyCrypto.openorders(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} orderns: {1}").format(
                                     symbol,
                                     orders))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def buy(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='buy'):
        return 1
    logger.log(msg='/buy', level=logging.INFO)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("Sorry, this isn't working now"))


def sell(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='sell'):
        return 1
    logger.log(msg='/sell', level=logging.INFO)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("Sorry, this isn't working now"))


def cancel(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='cancel'):
        return 1
    logger.log(msg='/cancel', level=logging.INFO)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("Sorry, this isn't working now"))


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
