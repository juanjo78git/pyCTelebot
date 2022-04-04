# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext

# i18n
_ = gettext.gettext

# Logs
logger = logging.getLogger(__name__)
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
    # Do something

    logger.log(msg='pyPoC run_telegram stop ID: {0}'.format(seed), level=logging.INFO)


def run():
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run start ID: {0}'.format(seed), level=logging.INFO)
    # Do something

    logger.log(msg='pyPoC run stop ID: {0}'.format(seed), level=logging.INFO)
