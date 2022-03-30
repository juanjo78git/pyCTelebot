# -*- coding: utf-8 -*-

from ccxt import binance
from pyCTelebot.config.auth import TOKEN_CRYPTO_KEY, TOKEN_CRYPTO_SECRET, TOKEN_CRYPTO_KEY_RO, TOKEN_CRYPTO_SECRET_RO
import gettext
import ccxt
import logging

# i18n
_ = gettext.gettext

# Binance connection
# exchange = ccxt.binance({
#     'apiKey': TOKEN_CRYPTO_KEY,
#     'secret': TOKEN_CRYPTO_SECRET
# })

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def connection(user='READONLY'):
    # Binance connection
    logger.log(msg='Exchange connection user: {0}'.format(user), level=logging.INFO)
    if user == 'READONLY':
        exchange = ccxt.binance({
            'apiKey': TOKEN_CRYPTO_KEY_RO,
            'secret': TOKEN_CRYPTO_SECRET_RO
        })
    else:
        exchange = ccxt.binance({
            'apiKey': TOKEN_CRYPTO_KEY,
            'secret': TOKEN_CRYPTO_SECRET
        })
    # enable rate limiting
    # exchange.enableRateLimit = True
    return exchange


def price(symbol, exchange=connection()):
    last_price = exchange.fetch_ticker(symbol=symbol).get('last')
    logger.log(msg='Search price {0} --> value: {1}'.format(symbol, last_price), level=logging.INFO)
    # Return
    return last_price


def open_orders(symbol, exchange=connection()):
    orders = exchange.fetch_open_orders(symbol=symbol)
    logger.log(msg='Open orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.INFO)
    # Return
    return orders


def closed_orders(symbol, exchange=connection()):
    orders = exchange.fetch_closed_orders(symbol=symbol)
    logger.log(msg='Closed orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.INFO)
    # Return
    return orders


def balance(symbol='ALL_BALANCES', exchange=connection()):
    balances = exchange.fetch_total_balance()
    all_balances = {}
    for key in balances:
        if balances[key] != 0:
            all_balances[key] = balances[key]
    if symbol == 'ALL_BALANCES':
        logger.log(msg='All balances:  {0}'.format(all_balances), level=logging.INFO)
        return all_balances
    else:
        logger.log(msg='Balance: symbol {0} - Value: {1}'.format(symbol, balances[symbol]), level=logging.INFO)
        # Return
        return balances[symbol]


def cancel_order(orderid, symbol, exchange=connection()):
    try:
        exchange.cancel_order(id=orderid, symbol=symbol)
        status = 'OK'
    except BaseException as err:
        # Like OrderNotFound exception
        status = str(err)

    logger.log(msg='Order {0} - {1}: status: {2}'.format(orderid, symbol, status), level=logging.INFO)
    # Return
    return status


def buy_order(symbol, amount, type_order, price_limit=0, exchange=connection()):
    try:
        if type_order == 'market':
            status = exchange.create_market_buy_order(symbol=symbol, amount=amount)
        elif type_order == 'limit':
            status = exchange.create_limit_buy_order(symbol=symbol, amount=amount, price=price_limit)
        else:
            status = 'ERROR: Type (market or limit)'
    except BaseException as err:
        status = str(err)
    logger.log(msg='Order {0} - {1} - {2} ({3}): status: {4}'.format(type_order, symbol, amount, price_limit, status),
               level=logging.INFO)
    # Return
    return status


def sell_order(symbol, amount, type_order, price_limit=0, exchange=connection()):
    try:
        if type == 'market':
            status = exchange.create_market_sell_order(symbol=symbol, amount=amount)
        elif type == 'limit':
            status = exchange.create_limit_sell_order(symbol=symbol, amount=amount, price=price_limit)
        else:
            status = 'ERROR: Type (market or limit)'
    except BaseException as err:
        status = str(err)
    logger.log(msg='Order {0} - {1} - {2} ({3}): status: {4}'.format(type_order, symbol, amount, price_limit, status),
               level=logging.INFO)
    # Return
    return status
