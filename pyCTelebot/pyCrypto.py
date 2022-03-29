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


def price(symbol):
    last_price = exchange.fetch_ticker(symbol=symbol).get('last')
    logger.log(msg='Search price {0} --> value: {1}'.format(symbol, last_price), level=logging.INFO)
    # Return
    return last_price


def open_orders(symbol):
    orders = exchange.fetch_open_orders(symbol=symbol)
    logger.log(msg='Open orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.INFO)
    # Return
    return orders


def closed_orders(symbol):
    orders = exchange.fetch_closed_orders(symbol=symbol)
    logger.log(msg='Closed orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.INFO)
    # Return
    return orders


def balance(symbol):
    balances = exchange.fetch_balance()
    selected = {}
    logger.log(msg='Balances: {0}'.format(balances), level=logging.INFO)
    for b in str(balances).strip('[]').replace('{', '').split('}'):
        logger.log(msg='Balance: {0}'.format(b), level=logging.INFO)
        if b.find(symbol) >= 0:
            selected = selected + b + '\n'
    logger.log(msg='Balance: symbol {0} - Value: {1}'.format(symbol, selected), level=logging.INFO)
    # Return
    return selected


def cancel_order(orderid, symbol):
    try:
        exchange.cancel_order(id=orderid, symbol=symbol)
        status = 'OK'
    except BaseException as err:
        # Like OrderNotFound exception
        status = str(err)

    logger.log(msg='Order {0} - {1}: status: {2}'.format(orderid, symbol, status), level=logging.INFO)
    # Return
    return status


def buy_order(symbol, amount, type_order, price=0):
    try:
        if type_order == 'market':
            status = exchange.create_market_buy_order(symbol=symbol, amount=amount)
        elif type_order == 'limit':
            status = exchange.create_limit_buy_order(symbol=symbol, amount=amount, price=price)
        else:
            status = 'ERROR: Type (market or limit)'
    except BaseException as err:
        status = str(err)
    logger.log(msg='Order {0} - {1} - {2} ({3}): status: {4}'.format(type_order, symbol, amount, price, status),
               level=logging.INFO)
    # Return
    return status


def sell_order(symbol, amount, type_order, price=0):
    try:
        if type == 'market':
            status = exchange.create_market_sell_order(symbol=symbol, amount=amount)
        elif type == 'limit':
            status = exchange.create_limit_sell_order(symbol=symbol, amount=amount, price=price)
        else:
            status = 'ERROR: Type (market or limit)'
    except BaseException as err:
        status = str(err)
    logger.log(msg='Order {0} - {1} - {2} ({3}): status: {4}'.format(type_order, symbol, amount, price, status),
               level=logging.INFO)
    # Return
    return status
