# -*- coding: utf-8 -*-


from telegram.ext import Updater
from telegram import Update, Bot
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from pyCTelebot.config.auth import TOKEN_TELEGRAM, WEBHOOK_URL_TELEGRAM, PORT, ENV_CONFIG, TELEGRAM_ADMIN_GROUP, users
from pyCTelebot import pyCrypto
from pyCTelebot.config import __version__
import gettext
import logging

# i18n
_ = gettext.gettext
# Logs
logger = logging.getLogger(__name__)
# DEBUG / INFO / WARNING / ERROR / CRITICAL
if ENV_CONFIG.get('log') == 'CRITICAL':
    logger.setLevel(logging.CRITICAL)
elif ENV_CONFIG.get('log') == 'ERROR':
    logger.setLevel(logging.ERROR)
elif ENV_CONFIG.get('log') == 'WARNING':
    logger.setLevel(logging.WARNING)
elif ENV_CONFIG.get('log') == 'INFO':
    logger.setLevel(logging.INFO)
else:
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

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

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

    message_admins_by_telegram_handler = CommandHandler('message_admins', message_admins_by_telegram)
    dispatcher.add_handler(message_admins_by_telegram_handler)

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
# def echo(update: Update, context: CallbackContext):
#     logger.log(msg='User ({0}): {1} chat: {2}'.format(update.effective_user.name,
#                                                       update.effective_user.id,
#                                                       update.effective_chat.id),
#                level=logging.INFO)
#      if not authorization(update=update, context=context, action='echo'):
#          return 1
#      context.bot.send_message(chat_id=update.effective_chat.id, text=_("{0} said: {1}").format(
#         update.effective_user.first_name, update.message.text))
#     return 1


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
    message_admins - Send message to admins
    help - Help command
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
                                    "/message_admins [MESSAGE] - Send message to admins \n"
                                    "/help  - This help (version {0})").format(__version__))


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
                                     text=_("Trading pair: {0} price --> {1} {2}").format(
                                         symbol,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                     text=_("Balance {0} --> {1} {2}").format(
                                         symbol,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                     text=_("All balances --> {0} {1}").format(
                                         _("ERROR: I can't do it."),
                                         str(err)))


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
                                     text=_("Trading pair: {0} open orders --> {1} {2}").format(
                                         symbol,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                     text=_("Trading pair: {0} closed orders --> {1} {2}").format(
                                         symbol,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                     text=_("Buying order with symbol {0} and amount {1} --> {2}").format(
                                         symbol,
                                         amount,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Buying order with "
                                            "symbol {0} and amount {1} --> {2} {3}").format(
                                         symbol,
                                         amount,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                         "symbol {0}, amount {1} and price {2} --> {3}").format(
                                         symbol,
                                         amount,
                                         price_limit,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Create limit buy order with "
                                            "symbol {0} and amount {1} and price {2} --> {3} {4}").format(
                                         symbol,
                                         amount,
                                         price_limit,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                            "symbol {0} and amount {1} --> {2}").format(
                                         symbol,
                                         amount,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Selling order with "
                                            "symbol {0} and amount {1} --> {2} {3}").format(
                                         symbol,
                                         amount,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
                                         "symbol {0}, amount {1} and price {2} --> {3}").format(
                                         symbol,
                                         amount,
                                         price_limit,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Create limit sell order with "
                                            "symbol {0} and amount {1} and price {2} --> {3} {4}").format(
                                         symbol,
                                         amount,
                                         price_limit,
                                         _("ERROR: I can't do it."),
                                         str(err)))
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
        order_id = update.effective_message.text.split(' ')[2]
    elif len(update.effective_message.text.split(' ')) == 2 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        order_id = update.effective_message.text.split(' ')[1]
    if 'symbol' in locals() and 'order_id' in locals():
        logger.log(msg='/cancel symbol: {0}, order_id: {1}'.format(symbol, order_id), level=logging.INFO)
        try:
            status = pyCrypto.cancel_order(order_id=order_id, symbol=symbol, user=update.effective_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Canceling order with "
                                            "symbol {0} and id {1} --> {2}").format(
                                         symbol,
                                         order_id,
                                         status))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("Canceling order with "
                                            "symbol {0} and id {1} --> {2} {3}").format(
                                         symbol,
                                         order_id,
                                         _("ERROR: I can't do it."),
                                         str(err)))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def unknown(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Sorry, I didn't understand that command."))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def message_admins_by_telegram(update: Update, context: CallbackContext):
    if not authorization(update=update, context=context, action='message_admin'):
        return 1
    logger.log(msg='/message_admin', level=logging.INFO)
    if len(update.effective_message.text.split(' ')) == 2:
        message = update.effective_message.text.split(' ')[1]
        user = update.effective_user.name
        user_id = update.effective_user.id
        chat = update.effective_chat.title
        chat_id = update.effective_chat.id
        message_admins(_("{0} ({1}) in chat {2} ({3}) said: {4}").format(user, user_id, chat, chat_id, message))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))


def private_message_admins(message):
    for user in users('ADMIN'):
        bot = Bot(token=TOKEN_TELEGRAM)
        try:
            bot.send_message(chat_id=user['telegram_id'], text=message)
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def message_admins(message):
    for group_id in TELEGRAM_ADMIN_GROUP:
        bot = Bot(token=TOKEN_TELEGRAM)
        try:
            bot.send_message(chat_id=group_id, text=message)
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def private_message(message, user):
    bot = Bot(token=TOKEN_TELEGRAM)
    try:
        bot.send_message(chat_id=user['telegram_id'], text=message)
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def authorization(update: Update, context: CallbackContext, action: str):
    logger.log(msg='authorization - User: {0} action: {1}'.format(update.effective_user.id, action), level=logging.INFO)
    try:
        if next((user for user in users('ADMIN') if user['telegram_id'] == str(update.effective_user.id)), None):
            return True
        if (next((user for user in users('USER') if user['telegram_id'] == str(update.effective_user.id)), None)) \
                and action == 'message_admin':
            return True
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("You can't do it!"))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        logger.log(msg='authorization: {0}'.format(str(err)), level=logging.ERROR)
    return False
