# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext
from pyCTelebot.config.auth import ENV_CONFIG

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


def run_telegram(update: Update, context: CallbackContext):
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run_telegram start ID: {0}'.format(seed), level=logging.INFO)
    logger.log(msg='/poc User {0} ({1}) - chat: {2} ({3}) - message ({4}) {5}'.format(update.effective_user.name,
                                                                                      update.effective_user.id,
                                                                                      update.effective_chat.title,
                                                                                      update.effective_chat.id,
                                                                                      update.message.text,
                                                                                      len(context.args)),
               level=logging.DEBUG)
    if logger.level == logging.DEBUG:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/poc User {0} ({1}) - chat: {2} ({3}) - message ({4}) {5}'.format(
                                     update.effective_user.name,
                                     update.effective_user.id,
                                     update.effective_chat.title,
                                     update.effective_chat.id,
                                     update.message.text,
                                     len(context.args)))
    # Do something

    logger.log(msg='pyPoC run_telegram stop ID: {0}'.format(seed), level=logging.INFO)


def run():
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run start ID: {0}'.format(seed), level=logging.INFO)
    # Do something

    logger.log(msg='pyPoC run stop ID: {0}'.format(seed), level=logging.INFO)
