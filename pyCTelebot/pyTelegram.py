# -*- coding: utf-8 -*-


from telegram.ext import Updater
from telegram import Update, Bot
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from pyCTelebot.config.auth import TOKEN_TELEGRAM, WEBHOOK_URL_TELEGRAM, PORT, users
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
    # Connection
    updater = Updater(token=TOKEN_TELEGRAM, use_context=True)
    dispatcher = updater.dispatcher

    # Events that will trigger this bot
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

    balance_handler = CommandHandler('balance', balance)
    dispatcher.add_handler(balance_handler)

    open_orders_handler = CommandHandler('open_orders', open_orders)
    dispatcher.add_handler(open_orders_handler)

    closed_orders_handler = CommandHandler('closed_orders', closed_orders)
    dispatcher.add_handler(closed_orders_handler)

    buy_handler = CommandHandler('buy', buy)
    dispatcher.add_handler(buy_handler)

    buy_limit_handler = CommandHandler('buy_limit', buy_limit)
    dispatcher.add_handler(buy_limit_handler)

    sell_handler = CommandHandler('sell', sell)
    dispatcher.add_handler(sell_handler)

    sell_limit_handler = CommandHandler('sell_limit', sell_limit)
    dispatcher.add_handler(sell_limit_handler)

    cancel_order_handler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancel_order_handler)

    # Unknown commands
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Error handler
    dispatcher.add_error_handler(error_callback)

    # Start this bot
    if how == 'w':
        logger.log(msg='Start with webhook', level=logging.INFO)
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN_TELEGRAM,
                              webhook_url=WEBHOOK_URL_TELEGRAM + TOKEN_TELEGRAM)
    else:
        logger.log(msg='Start with polling', level=logging.INFO)
        updater.start_polling()

    # Keep it from stopping
    updater.idle()


def start(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='start'):
        return 1
    if len(update.effective_message.text.split(' ')) == 2:
        symbol = update.effective_message.text.split(' ')[1].upper()
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


# Eco
def echo(update: Update, context: CallbackContext):
    # if not authorization(update=update, context=context, action='echo'):
    #     return 1
    # context.bot.send_message(chat_id=update.effective_chat.id, text=_("{0} said: {1}").format(
    #    update.effective_user.first_name, update.message.text))
    return 1


def help_command(update: Update, context: CallbackContext):
    """
    @BotFather /setcommands
    start - Select a trading pair to work
    stop - Clean all
    price - Current trading pair price
    balance - Show current balance
    open_orders - Show all open orders for the trading pair
    closed_orders - Show all closed orders for the trading pair
    buy - Send a new purchase order
    buy_limit - Send a new limit purchase order
    sell - Send a new sales order
    sell_limit - Send a new limit sales order
    cancel - Cancel open order
    help - This help
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("You can control me by sending these commands: \n"
                                    "\n"
                                    "/start [SYMBOL] - Select a trading pair to work \n"
                                    "/stop - Clean all \n"
                                    "/price [SYMBOL] - Current trading pair price \n"
                                    "/balance [SYMBOL] - Current balance, without params show all balances \n"
                                    "/open_orders [SYMBOL] - Show all open orders for the trading pair \n"
                                    "/closed_orders [SYMBOL] - Show all closed orders for the trading pair \n"
                                    "/buy [SYMBOL] [AMOUNT] - Send a new purchase order \n"
                                    "/buy_limit [SYMBOL] [AMOUNT] [PRICE] - Send a new limit purchase order \n"
                                    "/sell [SYMBOL] [AMOUNT] - Send a new sales order \n"
                                    "/sell_limit [SYMBOL] [AMOUNT] [PRICE] - Send a new limit sales order \n"
                                    "/cancel [SYMBOL] [ORDER ID] - Cancel open order \n"
                                    "/help  - This help"))


def price(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='price'):
        return 1
    if len(update.effective_message.text.split(' ')) == 2:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(update.effective_message.text.split(' ')) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]

    if 'symbol' in locals():
        logger.log(msg='/price symbol used: {0}'.format(symbol), level=logging.INFO)
        try:
            last_price = pyCrypto.price(symbol=symbol, user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Trading pair: {0} Last price: {1}").format(
                                         symbol,
                                         last_price))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Trading pair: {0} price --> status {1}").format(
                                         symbol,
                                         _("ERROR: I can't do it")))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def balance(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='balance'):
        return 1
    if len(update.effective_message.text.split(' ')) == 2:
        symbol = update.effective_message.text.split(' ')[1].upper()
    elif len(update.effective_message.text.split(' ')) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"].split('/')[0]
    if 'symbol' in locals():
        logger.log(msg='/balance symbol used: {0}'.format(symbol), level=logging.INFO)
        try:
            balances = pyCrypto.balance(symbol=symbol, user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Symbol: {0} Balance: {1}").format(
                                          symbol,
                                          balances))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Balance {0} --> status {1}").format(
                                         symbol,
                                         _("ERROR: I can't do it")))
    else:
        try:
            balances = pyCrypto.balance(user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("All balances: {0}").format(
                                         balances))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("All balances --> status {0}").format(
                                         _("ERROR: I can't do it")))


def open_orders(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='open_orders'):
        return 1
    if len(update.effective_message.text.split(' ')) == 2:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(update.effective_message.text.split(' ')) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]

    if 'symbol' in locals():
        logger.log(msg='/open_orders symbol used: {0}'.format(symbol), level=logging.INFO)
        try:
            orders = pyCrypto.open_orders(symbol=symbol, user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Trading pair: {0} open orders: {1}").format(
                                         symbol,
                                         orders))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Trading pair: {0} open orders --> status {1}").format(
                                         symbol,
                                         _("ERROR: I can't do it")))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def closed_orders(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='closed_orders'):
        return 1
    if len(update.effective_message.text.split(' ')) == 2:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(update.effective_message.text.split(' ')) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]

    if 'symbol' in locals():
        logger.log(msg='/closed_orders symbol used: {0}'.format(symbol), level=logging.INFO)
        try:
            orders = pyCrypto.closed_orders(symbol=symbol, user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Trading pair: {0} closed orders: {1}").format(
                                         symbol,
                                         orders))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Trading pair: {0} closed orders --> status {1}").format(
                                         symbol,
                                         _("ERROR: I can't do it")))
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
        try:
            status = pyCrypto.buy_order(symbol=symbol,
                                        amount=amount,
                                        type_order='market',
                                        user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Buying order with symbol {0} and amount {1} --> status {2}").format(
                                         symbol,
                                         amount,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Buying order with "
                                            "symbol {0} and amount {1} --> status {2}").format(
                                         symbol,
                                         amount,
                                         _("ERROR: I can't do it")))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def buy_limit(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='buy_limit'):
        return 1
    logger.log(msg='/buy_limit', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 4:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = update.effective_message.text.split(' ')[2]
        price_limit = update.effective_message.text.split(' ')[3]
    elif len(update.effective_message.text.split(' ')) == 3 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = update.effective_message.text.split(' ')[1]
        price_limit = update.effective_message.text.split(' ')[2]
    if 'symbol' in locals() and 'amount' in locals() and 'price_limit' in locals():
        logger.log(msg='/buy_limit symbol: {0}, amount: {1}, price: {2}'.format(symbol, amount, price_limit),
                   level=logging.INFO)
        try:
            status = pyCrypto.buy_order(symbol=symbol,
                                        amount=amount,
                                        type_order='limit',
                                        price_limit=price_limit,
                                        user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_(
                                         "Create limit buy order with "
                                         "symbol {0}, amount {1} and price {2} --> status {3}").format(
                                         symbol,
                                         amount,
                                         price_limit,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Create limit buy order with "
                                            "symbol {0} and amount {1} and price {2} --> status {3}").format(
                                             symbol,
                                             amount,
                                             price_limit,
                                             _("ERROR: I can't do it")))
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
        try:
            status = pyCrypto.sell_order(symbol=symbol,
                                         amount=amount,
                                         type_order='market',
                                         user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Selling order with "
                                            "symbol {0} and amount {1} --> status {2}").format(
                                             symbol,
                                             amount,
                                             status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Selling order with "
                                            "symbol {0} and amount {1} --> status {2}").format(
                                             symbol,
                                             amount,
                                             _("ERROR: I can't do it")))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def sell_limit(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='sell_limit'):
        return 1
    logger.log(msg='/sell_limit', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 4:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = update.effective_message.text.split(' ')[2]
        price_limit = update.effective_message.text.split(' ')[3]
    elif len(update.effective_message.text.split(' ')) == 3 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = update.effective_message.text.split(' ')[1]
        price_limit = update.effective_message.text.split(' ')[2]
    if 'symbol' in locals() and 'amount' in locals() and 'price_limit' in locals():
        logger.log(msg='/sell_limit symbol: {0}, amount: {1}, price: {2}'.format(symbol, amount, price_limit),
                   level=logging.INFO)
        try:
            status = pyCrypto.sell_order(symbol=symbol,
                                         amount=amount,
                                         type_order='limit',
                                         price_limit=price_limit,
                                         user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_(
                                         "Create limit sell order with "
                                         "symbol {0}, amount {1} and price {2}--> status {3}").format(
                                         symbol,
                                         amount,
                                         price_limit,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Create limit sell order with "
                                            "symbol {0} and amount {1} and price {2} --> status {3}").format(
                                             symbol,
                                             amount,
                                             price_limit,
                                             _("ERROR: I can't do it")))
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
        try:
            status = pyCrypto.cancel_order(orderid=orderid, symbol=symbol, user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Canceling order with "
                                            "symbol {0} and id {1} --> status {2}").format(
                                             symbol,
                                             orderid,
                                             status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Canceling order with "
                                            "symbol {0} and id {1} --> status {2}").format(
                                             symbol,
                                             orderid,
                                             _("ERROR: I can't do it")))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def unknown(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Sorry, I didn't understand that command."))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def private_message_admins(message):
    for user in users('ADMIN'):
        bot = Bot(token=TOKEN_TELEGRAM)
        try:
            bot.send_message(chat_id=user['telegramid'], text=message)
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def private_message(message, user):
    bot = Bot(token=TOKEN_TELEGRAM)
    try:
        bot.send_message(chat_id=user['telegramid'], text=message)
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def authorization(update: Update, context: CallbackContext, action):
    logger.log(msg='User: {0} action: {1}'.format(update.effective_user.id, action), level=logging.INFO)

    if next((user for user in users('ADMIN') if user['telegramid'] == str(update.effective_user.id)), None):
        return True
    else:
        try:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("You can't do it!"))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        return False
