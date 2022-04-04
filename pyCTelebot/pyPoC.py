# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext
import telegram
from pyCTelebot.config.auth import ENV_CONFIG
import psutil

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
# Force DEBUG
logger.setLevel(logging.DEBUG)


# Telegram Proof of Concept
def run_telegram(update: Update, context: CallbackContext):
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run_telegram start ID: {0}'.format(seed), level=logging.INFO)
    logger.log(msg='/poc User {0} ({1}) - chat: {2} ({3}) - message ({4}) {5}'.format(update.effective_user.name,
                                                                                      update.effective_user.id,
                                                                                      update.effective_chat.title,
                                                                                      update.effective_chat.id,
                                                                                      len(context.args),
                                                                                      update.message.text),
               level=logging.DEBUG)
    if logger.level == logging.DEBUG:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/poc User {0} ({1}) - chat: {2} ({3}) - message ({4}) {5}'.format(
                                     update.effective_user.name,
                                     update.effective_user.id,
                                     update.effective_chat.title,
                                     update.effective_chat.id,
                                     len(context.args),
                                     update.message.text))
    # Do something

    logger.log(msg='pyPoC run_telegram stop ID: {0}'.format(seed), level=logging.INFO)
    keyboard = [[telegram.InlineKeyboardButton('Option ETH', callback_data='/start eth')],
                [telegram.InlineKeyboardButton('Option BTC', callback_data='/start btc')]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text('*****Menu*****\nOptions:', reply_markup=reply_markup,
                              reply_to_message_id=update.message.message_id)

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
    for p in psutil.process_iter():
        try:
            if 'PY' in str(p).upper():
                logger.log(msg='pyPoC PS: {0} - {1}'.format(p.pid, p.cmdline()), level=logging.INFO)
        except Exception:
            logger.log(msg='pyPoC run stop/KILLED ID: {0}'.format(seed), level=logging.INFO)
    logger.log(msg='pyPoC run stop ID: {0}'.format(seed), level=logging.INFO)


# Telegram Proof of Concept
def ps(update: Update, context: CallbackContext):
    for p in psutil.process_iter():
        try:
            if 'PY' in str(p).upper():
                logger.log(msg='pyPoC PS: {0} - {1}'.format(p.pid, p.cmdline()), level=logging.INFO)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='/ps {0} - {1}'.format(
                                             p.pid,
                                             p.cmdline()))
        except Exception:
            logger.log(msg='pyPoC run stop/KILLED ID: {0}'.format(seed), level=logging.INFO)
