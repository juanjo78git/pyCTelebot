# -*- coding: utf-8 -*-

from pyCTelebot.config.auth import TOKEN_CRYPTO_KEY, TOKEN_CRYPTO_SECRET
from pyCTelebot import pyCrypto, pyTelegram
from datetime import datetime
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
    logger.log(msg='CryptoWorker doing something!', level=logging.INFO)
    #symbol = 'ETH/USDT'
    # last_price = pyCrypto.price(symbol=symbol)
    # Send results
    # logger.log(msg='Worker - Symbol: {0} --> value: {1}'.format(symbol, last_price), level=logging.INFO)

    pyTelegram.private_message_admin(message='Worker: {0}'.format(datetime.now()))
