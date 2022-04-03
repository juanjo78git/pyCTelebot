# -*- coding: utf-8 -*-
import os

from pyCTelebot import pyCrypto, pyTelegram
from datetime import datetime
import gettext
import logging
from pyCTelebot.config.auth import ENV_CONFIG
import pytz
from time import sleep
import random
import sys
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
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='Worker start ID: {0}'.format(seed), level=logging.INFO)
    pyTelegram.message_admins(message='Worker start at {0} with ID: {1}'.format(
        datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))
    sleep(50)
    logger.log(msg='Worker stop ID: {0}'.format(seed), level=logging.INFO)
    pyTelegram.message_admins(message='Worker stop at {0} with ID: {1}'.format(
        datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))


def alert_worker():
    logger.log(msg='alert_worker doing something!', level=logging.INFO)
    symbol = os.environ.get('SYMBOL_TEST', 'ETH/USDT')
    ticker = pyCrypto.price(symbol=symbol)
    # period
    sleep(int(os.environ.get('PERIOD_TEST', '520')))
    ticker2 = pyCrypto.price(symbol=symbol)
    # Send results
    # logger.log(msg='Worker - Symbol: {0} --> value: {1}'.format(symbol, ticker), level=logging.INFO)
    percent = float(os.environ.get('PERCENT_TEST', '1'))
    # bid: current best buy price // ask: current best sell price
    price_name_list = ["bid", "ask"]
    for price_name in price_name_list:
        old_price = ticker.get(price_name)
        new_price = ticker2.get(price_name)
        percent_dif_price = (new_price - old_price) * 100 / new_price

        if percent < abs(percent_dif_price) and percent_dif_price > 0:
            pyTelegram.message_admins(message='WorkerTelegram: {0} Symbol {1} '
                                              '{2} PRICE DOWN OVER {3}%!! {4} - {5}'.format(
                                                datetime.now(tz=pytz.timezone("Europe/Madrid")),
                                                symbol,
                                                price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                                                percent_dif_price,
                                                new_price,
                                                old_price))
            logger.log(msg='WorkerTelegram: {0} Symbol {1} {2} PRICE UP OVER {3}%!! {4} - {5}'.format(
                        datetime.now(tz=pytz.timezone("Europe/Madrid")),
                        symbol,
                        price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                        percent_dif_price,
                        new_price,
                        old_price
                        ), level=logging.INFO)
        elif percent < abs(percent_dif_price) and percent_dif_price < 0:
            pyTelegram.message_admins(message='WorkerTelegram: {0} Symbol {1} '
                                              '{2} PRICE DOWN OVER {3}%!! {4} - {5}'.format(
                                                datetime.now(tz=pytz.timezone("Europe/Madrid")),
                                                symbol,
                                                price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                                                percent_dif_price,
                                                new_price,
                                                old_price))
            logger.log(msg='WorkerTelegram: {0} Symbol {1} {2} PRICE DOWN OVER {3}%!! {4} - {5}'.format(
                        datetime.now(tz=pytz.timezone("Europe/Madrid")),
                        symbol,
                        price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                        percent_dif_price,
                        new_price,
                        old_price
                        ), level=logging.INFO)
        else:
            # pyTelegram.message_admins(message='WorkerTelegram: {0} Symbol {1} '
            #                                   '{2}  PRICE NOT CHANGE A {3}% only a {4}%!! {5} - {6}'.format(
            #                                     datetime.now(tz=pytz.timezone("Europe/Madrid")),
            #                                     symbol,
            #                                     price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
            #                                     percent,
            #                                     percent_dif_price,
            #                                     new_price,
            #                                     old_price))
            logger.log(msg='WorkerTelegram: {0} Symbol {1} '
                           '{2} PRICE NOT CHANGE A {3}% only a {4}%!! {5} (Last: {6})'.format(
                            datetime.now(tz=pytz.timezone("Europe/Madrid")),
                            symbol,
                            price_name.replace("bid", "BUY").replace("ask", "SELL").upper(),
                            percent,
                            percent_dif_price,
                            new_price,
                            old_price
                            ), level=logging.INFO)
