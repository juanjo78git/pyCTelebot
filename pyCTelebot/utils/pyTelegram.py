# -*- coding: utf-8 -*-

from telegram.ext import Updater, CallbackQueryHandler
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from pyCTelebot.config.pyVars import TOKEN_TELEGRAM, WEBHOOK_URL_TELEGRAM, PORT, ENV_CONFIG, TELEGRAM_ADMIN_GROUP
from pyCTelebot.utils.pyUsers import user_list, authorization
from pyCTelebot.utils import pyCrypto, pyTemplates, pyPrices
from pyCTelebot import pyPoC
from pyCTelebot import __version__
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


def run(how: str):
    # Connection
    updater = Updater(token=TOKEN_TELEGRAM, use_context=True)
    dispatcher = updater.dispatcher

    # Events that will trigger this bot
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CallbackQueryHandler(callback_exchange, pattern='^(|kucoin|binance|kraken)$'))

    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)

    help_handler = CommandHandler('help', help_command)
    dispatcher.add_handler(help_handler)

    any_message_handler = MessageHandler(Filters.text & (~Filters.command), any_message)
    dispatcher.add_handler(any_message_handler)

    price_handler = CommandHandler('price', price)
    dispatcher.add_handler(price_handler)

    balance_handler = CommandHandler('balance', balance)
    dispatcher.add_handler(balance_handler)

    all_balance_handler = CommandHandler('all_balances', all_balances)
    dispatcher.add_handler(all_balance_handler)

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

    price_tracking_handler = CommandHandler('price_tracking', price_tracking)
    dispatcher.add_handler(price_tracking_handler)

    # PoC
    poc_handler = CommandHandler('poc', poc)
    dispatcher.add_handler(poc_handler)

    message_admins_by_telegram_handler = CommandHandler('message_admins', message_admins_by_telegram)
    dispatcher.add_handler(message_admins_by_telegram_handler)

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
        message_admins(_('Start pyCTelebot on telegram with webhook'))
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN_TELEGRAM,
                              webhook_url=WEBHOOK_URL_TELEGRAM + TOKEN_TELEGRAM)
    else:
        logger.log(msg='Start with polling', level=logging.INFO)
        message_admins(_('Start pyCTelebot on telegram with polling'))
        updater.start_polling(allowed_updates=[])

    # Keep it from stopping
    updater.idle()


def start(update: Update, context: CallbackContext):
    if not authorization(telegram_id=update.effective_user.id, action='start'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    if len(context.args) == 0:
        keyboard_exchange = [
            [InlineKeyboardButton("Kucoin", callback_data='kucoin'),
             InlineKeyboardButton("Binance", callback_data='binance'),
             InlineKeyboardButton("Kraken", callback_data='kraken'), ],
        ]
        update.message.reply_text(text=_('Please choose a exchange:'),
                                  reply_markup=InlineKeyboardMarkup(keyboard_exchange))
    elif len(context.args) == 1:
        exchange = context.args[0].lower()
        context.user_data["exchange"] = exchange
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Selected exchange: {0}").format(exchange))
    elif len(context.args) == 2:
        exchange = context.args[0].lower()
        context.user_data["exchange"] = exchange
        symbol = context.args[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        context.user_data["symbol"] = symbol
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Selected exchange: {0} and trading pair: {1}").format(exchange, symbol))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Hello!"))


def callback_exchange(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    exchange = query.data
    context.user_data["exchange"] = exchange
    query.message.edit_text(text=_("Selected exchange: {0}").format(exchange),
                            reply_markup=InlineKeyboardMarkup([]))


def stop(update: Update, context: CallbackContext):
    if not authorization(telegram_id=update.effective_user.id, action='stop'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    context.user_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=_("Bye!!"))


def any_message(update: Update, context: CallbackContext):
    logger.log(msg='User {0} ({1}) - chat: {2} ({3}) - message {4}'.format(update.effective_user.name,
                                                                           update.effective_user.id,
                                                                           update.effective_chat.title,
                                                                           update.effective_chat.id,
                                                                           update.message.text),
               level=logging.DEBUG)
    if not authorization(telegram_id=update.effective_user.id, action='any_message'):
        return 1
    # Do something with messages
    pyPoC.any_message_poc(update=update, context=context)


def help_command(update: Update, context: CallbackContext):
    """
    @BotFather /setcommands
    start - Select an exchange and trading pair to work
    stop - Clean all
    price - Current trading pair price
    balance - Show current balance
    all_balances - Current balance in all exchanges
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
                                    "/start [EXCHANGE] [SYMBOL] - Select  an exchange and trading pair to work \n"
                                    "/stop - Clean all \n"
                                    "/price [SYMBOL] - Current trading pair price \n"
                                    "/balance [SYMBOL] - Current balance, without params show all balances \n"
                                    "/all_balances [SYMBOL] - Current balance in all exchanges \n"
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
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='price'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 1:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(context.args) == 0 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/price symbol used: {0}'.format(symbol), level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        last_price = my_crypto.price(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} Last price: {1}").format(
                                     symbol,
                                     pyTemplates.templates_json(last_price, 'price')))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} price --> {1} {2}").format(
                                     symbol,
                                     _("ERROR: I can't do it."),
                                     str(err)))


def balance(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='balance'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
    if len(context.args) == 1:
        symbol = context.args[0].upper()
    elif len(context.args) == 0 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"].split('/')[0]
    # Action without params
    else:
        try:
            balances = my_crypto.balance()
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("All balances: {0}").format(
                                         pyTemplates.templates_json(balances, 'all_balances')))
        except TelegramError as err:
            logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=_("All balances --> {0} {1}").format(
                                         _("ERROR: I can't do it."),
                                         str(err)))
        return 1
    # Action with params
    logger.log(msg='/balance symbol used: {0}'.format(symbol), level=logging.DEBUG)
    try:
        balances = my_crypto.balance(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Symbol: {0} Balance: {1}").format(
                                     symbol,
                                     pyTemplates.templates_json(balances, 'balance')))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Balance {0} --> {1} {2}").format(
                                     symbol,
                                     _("ERROR: I can't do it."),
                                     str(err)))


def all_balances(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='balance'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    try:
        balances = pyCrypto.balance_all_exchanges(telegram_id=update.effective_user.id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("All balances: {0}").format(
                                     pyTemplates.templates_json(balances, 'all_balances')))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("All balances --> {0} {1}").format(
                                     _("ERROR: I can't do it."),
                                     str(err)))
    return 1


def open_orders(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='open_orders'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 1:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(context.args) == 0 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/open_orders symbol used: {0}'.format(symbol), level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        orders = my_crypto.open_orders(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} open orders: {1}").format(
                                     symbol,
                                     pyTemplates.templates_json(orders, 'open_orders')))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} open orders --> {1} {2}").format(
                                     symbol,
                                     _("ERROR: I can't do it."),
                                     str(err)))


def closed_orders(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='closed_orders'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 1:
        symbol = update.effective_message.text.split(' ')[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(context.args) == 0 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/closed_orders symbol used: {0}'.format(symbol), level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        orders = my_crypto.closed_orders(symbol=symbol)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} closed orders: {1}").format(
                                     symbol,
                                     pyTemplates.templates_json(orders, 'closed_orders')))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Trading pair: {0} closed orders --> {1} {2}").format(
                                     symbol,
                                     _("ERROR: I can't do it."),
                                     str(err)))


def buy(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='buy'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 2:
        symbol = context.args[1].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = context.args[1]
    elif len(context.args) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = context.args[0]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/buy symbol: {0}, amount: {1}'.format(symbol, amount), level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        status = my_crypto.buy_order(
            symbol=symbol,
            amount=amount,
            type_order='market')
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


def buy_limit(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='buy_limit'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 3:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = context.args[1]
        price_limit = context.args[2]
    elif len(context.args) == 2 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = context.args[0]
        price_limit = context.args[1]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/buy_limit symbol: {0}, amount: {1}, price: {2}'.format(symbol, amount, price_limit),
               level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        status = my_crypto.buy_order(
            symbol=symbol,
            amount=amount,
            type_order='limit',
            price_limit=price_limit)
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


def sell(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='sell'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 2:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = context.args[1]
    elif len(context.args) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = context.args[0]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/sell symbol: {0}, amount: {1}'.format(symbol, amount), level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        status = my_crypto.sell_order(symbol=symbol,
                                      amount=amount,
                                      type_order='market')
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


def sell_limit(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='sell_limit'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 3:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        amount = context.args[1]
        price_limit = context.args[2]
    elif len(context.args) == 2 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        amount = context.args[0]
        price_limit = context.args[1]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/sell_limit symbol: {0}, amount: {1}, price: {2}'.format(symbol, amount, price_limit),
               level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)

        status = my_crypto.sell_order(symbol=symbol,
                                      amount=amount,
                                      type_order='limit',
                                      price_limit=price_limit, )
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


def cancel(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='cancel'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 2:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
        order_id = context.args[1]
    elif len(context.args) == 1 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
        order_id = context.args[0]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/cancel symbol: {0}, order_id: {1}'.format(symbol, order_id), level=logging.DEBUG)
    try:
        my_crypto = pyCrypto.MyCrypto(exchange_name=exchange, telegram_id=update.effective_user.id)
        status = my_crypto.cancel_order(order_id=order_id,
                                        symbol=symbol)
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


def price_tracking(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='open_orders'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if context.user_data.get("exchange", None) is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You haven't selected exchange!"))
        return 1
    exchange = context.user_data["exchange"]
    if len(context.args) == 1:
        symbol = context.args[0].upper()
        if '/' not in symbol:
            symbol = symbol + '/USDT'
    elif len(context.args) == 0 and "symbol" in context.user_data:
        symbol = context.user_data["symbol"]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    logger.log(msg='/price_tracking exchange: {0} and symbol: {1}'.format(exchange, symbol), level=logging.DEBUG)
    try:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Added price tracking: {0} in {1}").format(symbol, exchange))
        pyPrices.initialize_price(exchange=exchange, symbol=symbol)
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Add price tracking: {0} in {1} --> {2} {3}").format(
                                     symbol, exchange,
                                     _("ERROR: I can't do it."),
                                     str(err)))


def unknown(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Sorry, I didn't understand that command."))
    except TelegramError as err:
        logger.log(msg='send_message: {0}'.format(str(err)), level=logging.ERROR)


def message_admins_by_telegram(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='message_admin'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Params
    if len(context.args) > 0:
        message = update.effective_message.text.split(sep=' ', maxsplit=1)[1]
        user = update.effective_user.name
        user_id = update.effective_user.id
        chat = update.effective_chat.title
        chat_id = update.effective_chat.id
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("Error: invalid parameters"))
        return 1
    # Action
    if chat_id == user_id:
        message_admins(_("{0} ({1}) said: {2}").format(user, user_id, message))
    else:
        message_admins(_("{0} ({1}) in chat {2} ({3}) said: {4}").format(user, user_id, chat, chat_id, message))


def private_message_admins(message):
    for user in user_list('ADMIN'):
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


def poc(update: Update, context: CallbackContext):
    # Authorization
    if not authorization(telegram_id=update.effective_user.id, action='poc'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_("You can't do it!"))
        return 1
    # Action
    pyPoC.run_telegram(update=update, context=context)
