# -*- coding: utf-8 -*-

from pyCTelebot import pyCrypto, pyTelegram
from datetime import datetime
import gettext
import logging
import pytz

# i18n
_ = gettext.gettext

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    logger.log(msg='CryptoWorker doing something!', level=logging.INFO)
    symbol = 'ETH/USDT'
    last_price = pyCrypto.price(symbol=symbol)
    # Send results
    # logger.log(msg='Worker - Symbol: {0} --> value: {1}'.format(symbol, last_price), level=logging.INFO)
    pyTelegram.private_message_admins(message='Worker: {0} UTC: {1} - {2}'.format(
        datetime.now(tz=pytz.timezone("Europe/Madrid")),
        datetime.now(),
        last_price))

