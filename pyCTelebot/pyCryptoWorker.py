# -*- coding: utf-8 -*-

from pyCTelebot.config.auth import TOKEN_CRYPTO_KEY, TOKEN_CRYPTO_SECRET
import gettext
import ccxt
import logging

# i18n
_ = gettext.gettext

# Binance connection
exchange = ccxt.binance({
    'apiKey': TOKEN_CRYPTO_KEY,
    'secret': TOKEN_CRYPTO_SECRET
})

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def run():
    logger.log(msg='CryptoWorker start!', level=logging.INFO)
