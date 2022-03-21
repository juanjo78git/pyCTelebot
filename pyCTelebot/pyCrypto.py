# -*- coding: utf-8 -*-


import gettext
_ = gettext.gettext

from pyCTelebot.config.auth import TOKEN_CRYPTO

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def price(coin):
    lastprice = 12.34
    logger.log(msg='Search price coin {0} with token: {1}'.format(coin, TOKEN_CRYPTO), level=logging.INFO)
    # Return
    return lastprice
