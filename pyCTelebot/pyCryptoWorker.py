# -*- coding: utf-8 -*-

from pyCTelebot import pyCrypto, pyTelegram
from datetime import datetime
import gettext
import logging
from pyCTelebot.config.auth import ENV_CONFIG
import pytz
from time import sleep

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


def run():
    logger.log(msg='CryptoWorker doing something!', level=logging.INFO)
    symbol = 'ETH/USDT'
    ticker = pyCrypto.price(symbol=symbol)
    sleep(10)
    ticker2 = pyCrypto.price(symbol=symbol)
    # Send results
    # logger.log(msg='Worker - Symbol: {0} --> value: {1}'.format(symbol, ticker), level=logging.INFO)
    percent = 1
    percent_value = 1 + percent/100
    # bid: current best buy price // ask: current best sell price
    price_name_list = ["bid", "ask"]
    for price_name in price_name_list:
        if ticker.get(price_name) > ticker2.get(price_name)*percent_value:
            # pyTelegram.message_admins(message='Worker: {0} Symbol {1} {2} PRICE UP OVER {3}%!! {4}'.format(
            logger.log(msg='WorkerTelegram: {0} Symbol {1} {2} PRICE UP OVER {3}%!! {4} - {5}'.format(
                datetime.now(tz=pytz.timezone("Europe/Madrid")),
                symbol,
                price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                percent,
                ticker.get(price_name),
                ticker2.get(price_name)
            ), level=logging.INFO)
        elif ticker.get(price_name)*percent_value < ticker2.get(price_name):
            # pyTelegram.message_admins(message='Worker: {0} Symbol {1} {2} PRICE DOWN OVER {3}!! {4}'.format(
            logger.log(msg='WorkerTelegram: {0} Symbol {1} {2} PRICE DOWN OVER {3}%!! {4} - {5}'.format(
                datetime.now(tz=pytz.timezone("Europe/Madrid")),
                symbol,
                price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                percent,
                ticker.get(price_name),
                ticker2.get(price_name)
            ), level=logging.INFO)
        else:
            logger.log(msg='WorkerTelegram: {0} Symbol {1} {2} PRICE NOT CHANGE A {3}%!! {4} - {5}'.format(
                datetime.now(tz=pytz.timezone("Europe/Madrid")),
                symbol,
                price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                percent,
                ticker.get(price_name),
                ticker2.get(price_name)
            ), level=logging.INFO)
