# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext
from pyCTelebot.config.pyVars import ENV_CONFIG

# i18n
from pyCTelebot.utils import pyPrices, pyTemplates

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


def run():
    """ Proof of Concept """
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run start ID: {0}'.format(seed), level=logging.INFO)
    # Do something

    logger.log(msg='pyPoC run stop ID: {0}'.format(seed), level=logging.INFO)


def run_telegram(update: Update, context: CallbackContext):
    """ Telegram Proof of Concept """
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run_telegram start ID: {0}'.format(seed), level=logging.INFO)
    prices = pyPrices.price_info()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=pyTemplates.templates_json(values=prices, template_type='prices'))
    logger.log(msg='pyPoC run_telegram stop ID: {0}'.format(seed), level=logging.INFO)


def any_message_poc(update: Update, context: CallbackContext):
    """ Telegram Proof of Concept: any message do it! """
    logger.log(msg='pyPoC any_message_poc start', level=logging.INFO)
    # Do something
    logger.log(msg='any_message_poc telegram_id: {0} name: {1} ({2}) '
                   'message: {3}'.format(update.effective_user.id,
                                         update.effective_user.name,
                                         update.effective_user.full_name,
                                         update.effective_message.text),
               level=logging.INFO)
