# -*- coding: utf-8 -*-

from pyCTelebot.config.auth import TOKEN_CRYPTO_KEY, TOKEN_CRYPTO_SECRET
import gettext
_ = gettext.gettext
# https://github.com/ccxt/ccxt
import ccxt
import json



import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def price(symbol):
    exchange = ccxt.binance({
        'apiKey': TOKEN_CRYPTO_KEY,
        'secret': TOKEN_CRYPTO_SECRET
    })
    symbol = symbol + '/USDT'
    lastprice = exchange.fetch_ticker(symbol=symbol).get('last')
    logger.log(msg='Search price {0} --> value: {1}'.format(symbol, lastprice), level=logging.INFO)
    # Return
    return lastprice
