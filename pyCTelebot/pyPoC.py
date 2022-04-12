# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext
from pyCTelebot.config.pyVars import ENV_CONFIG
import psutil

# i18n
from pyCTelebot.utils.pyPrices import initialize_price, price_info
from pyCTelebot.utils.pyUsers import user_list

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
# Force DEBUG
logger.setLevel(logging.DEBUG)


# Telegram Proof of Concept
def run_telegram(update: Update, context: CallbackContext):
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run_telegram start ID: {0}'.format(seed), level=logging.INFO)
    if len(context.args) == 2:
        exchange = context.args[0]
        symbol = context.args[1]
        logger.log(msg='pyPoC run_telegram: {0} - {1}'.format(exchange, symbol), level=logging.INFO)
        initialize_price(exchange=exchange, symbol=symbol)
        logger.log(msg='pyPoC initialize_price end', level=logging.INFO)
        price = price_info(exchange=exchange, symbol=symbol)
        logger.log(msg='pyPoC price_info end', level=logging.INFO)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/initialize_price OK: {0}'.format(price))
    elif len(context.args) == 1:
        symbol = context.args[0]
        price = price_info(symbol=symbol)
        logger.log(msg='pyPoC price_info end', level=logging.INFO)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/price_info: {0}'.format(price))
    else:
        price = price_info()
        logger.log(msg='pyPoC prices_info end', level=logging.INFO)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/prices_info: {0}'.format(price))
    logger.log(msg='pyPoC run_telegram stop ID: {0}'.format(seed), level=logging.INFO)


def poc_button(update: Update, context: CallbackContext):
    query = update.callback_query
    logger.log(msg='poc_button selected: {0}'.format(query.data), level=logging.INFO)
    context.bot.editMessageText(message_id=query.message.message_id,
                                chat_id=query.message.chat_id,
                                text=query.data)


# Proof of Concept
def run():
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run start ID: {0}'.format(seed), level=logging.INFO)
    # Do something
    print(user_list(role='READ_ONLY'))
    logger.log(msg='pyPoC run stop ID: {0}'.format(seed), level=logging.INFO)


# Telegram Proof of Concept ps
def ps(update: Update, context: CallbackContext):
    for p in psutil.process_iter():
        try:
            if 'PY' in str(p).upper():
                logger.log(msg='pyPoC PS: {0} - {1}'.format(p.pid, p.cmdline()), level=logging.INFO)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='/ps {0} - {1}'.format(
                                             p.pid,
                                             p.cmdline()))
        except Exception as err:
            logger.log(msg='pyPoC run stop/KILLED {0}'.format(str(err)), level=logging.INFO)


# Telegram Proof of Concept
def any_message_poc(update: Update, context: CallbackContext):
    logger.log(msg='pyPoC any_message_poc start', level=logging.INFO)
    # Do something
    logger.log(msg='any_message_poc telegram_id: {0} name: {1} ({2}) '
                   'message: {3} args: {4}'.format(update.effective_user.id,
                                                   update.effective_user.name,
                                                   update.effective_user.full_name,
                                                   update.effective_message.text,
                                                   context.args),
               level=logging.INFO)