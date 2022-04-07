# -*- coding: utf-8 -*-
from pyCTelebot import pyCrypto
from pyCTelebot.config.pyVars import ENV_CONFIG
import gettext
import logging
from pyCTelebot.utils.pyDB import MyDB

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


# exchange_prices table:
# { "exchange": "exchange",
#   "symbol": "symbol",
#   "last_buy_price": "last_buy_price",
#   "current_buy_price": "current_buy_price",
#   "buy_price_variation_percentage": "%",
#   "last_sell_price": "last_sell_price",
#   "current_sell_price": "current_sell_price",
#   "sell_price_variation_percentage": "%",
# }
def price_info(exchange: str = None, symbol: str = None):
    my_prices = []
    try:
        logger.log(msg='price_info - exchange: {0} - symbol: {1}'.format(exchange, symbol),
                   level=logging.DEBUG)
        if exchange is not None or symbol is not None:
            query = 'select * from exchange_prices where '
            args = []
            if exchange is not None:
                query += ' exchange = %s '
                args.append(exchange)
            if exchange is not None and symbol is not None:
                query += ' and '
            if symbol is not None:
                query += ' symbol = %s '
                args.append(str(symbol))
            db = MyDB()
            result = db.query(query=query, args=args)
            db.close()
            for my_price in result:
                my_prices.append(dict(my_price))
    except Exception as err:
        logger.log(msg='price_info: {0}'.format(str(err)), level=logging.ERROR)
    return my_prices


def price_variation_percentage(last_price: float, current_price: float):
    try:
        logger.log(msg='price_variation_percentage - last_price: {0} - current_price: {1}'.format(
            last_price,
            current_price),
            level=logging.DEBUG)
        if current_price <= 0:
            return None
        percent_dif_price = (current_price - last_price) * 100 / current_price
        return percent_dif_price
    except Exception as err:
        logger.log(msg='price_variation_percentage: {0}'.format(str(err)), level=logging.ERROR)
    return None


def update_price_info():
    logger.log(msg='update_price_info: Start', level=logging.DEBUG)
    for p in price_info():
        try:
            logger.log(msg='update_price_info - for {0}'.format(p), level=logging.DEBUG)
            current_price = pyCrypto.price(symbol=p['symbol'])
            logger.log(msg='update_price_info - result {0}'.format(current_price), level=logging.DEBUG)
            # TODO
        except Exception as err:
            logger.log(msg='update_price_info: {0}'.format(str(err)), level=logging.ERROR)
