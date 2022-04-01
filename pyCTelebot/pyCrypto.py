# -*- coding: utf-8 -*-

from ccxt import binance
from pyCTelebot.config.auth import TOKEN_CRYPTO_KEY_RO, TOKEN_CRYPTO_SECRET_RO, select_user
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
# Test Exchange
params = {}
# params = {'test': True}

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def connection(user='ME'):
    # Binance connection
    logger.log(msg='Exchange connection user: {0}'.format(user), level=logging.INFO)
    exchange = None
    try:
        if user == 'READONLY':
            exchange = ccxt.binance({
                'apiKey': TOKEN_CRYPTO_KEY_RO,
                'secret': TOKEN_CRYPTO_SECRET_RO
            })
        else:
            u = select_user(user=user, telegram_id=user)
            if u is None:
                raise Exception("User does not exist {0}".format(user))
            if u['exchange'] == 'binance':
                exchange = ccxt.binance({
                    'apiKey': u['apiKey'],
                    'secret': u['secret']
                })
        # enable rate limiting
        # exchange.enableRateLimit = True
    except Exception as err:
        logger.log(
            msg='connection {0}: status: {1} - {2}'.format(user,
                                                           type(err),
                                                           str(err)),
            level=logging.ERROR)
        raise
    else:
        return exchange


def price(symbol, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        last_price = exchange.fetch_ticker(symbol=symbol, params=params).get('last')
    except Exception as err:
        logger.log(
            msg='price {0}: status: {1} - {2}'.format(symbol,
                                                      type(err),
                                                      str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='Search price {0} --> value: {1}'.format(symbol, last_price), level=logging.INFO)
        return last_price


def open_orders(symbol, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        orders = exchange.fetch_open_orders(symbol=symbol, params=params)
    except Exception as err:
        logger.log(
            msg='open_orders {0}: status: {1} - {2}'.format(symbol,
                                                            type(err),
                                                            str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='Open orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.INFO)
        return orders


def closed_orders(symbol, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        orders = exchange.fetch_closed_orders(symbol=symbol, params=params)
    except Exception as err:
        logger.log(
            msg='closed_orders {0}: status: {1} - {2}'.format(symbol,
                                                              type(err),
                                                              str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='Closed orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.INFO)
        return orders


def balance(symbol=None, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        balances = exchange.fetch_total_balance(params=params)
        all_balances = {}
        for key in balances:
            if balances[key] != 0:
                all_balances[key] = balances[key]
    except Exception as err:
        logger.log(
            msg='balance {0}: status: {1} - {2}'.format(symbol,
                                                        type(err),
                                                        str(err)),
            level=logging.ERROR)
        raise
    else:
        if symbol is None:
            logger.log(msg='All balances:  {0}'.format(all_balances), level=logging.INFO)
            return all_balances
        else:
            logger.log(msg='Balance: symbol {0} - Value: {1}'.format(symbol, balances[symbol]), level=logging.INFO)
            return balances[symbol]


def cancel_order(orderid, symbol, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        status = exchange.cancel_order(id=orderid, symbol=symbol, params=params)
    except Exception as err:
        # Like OrderNotFound exception
        logger.log(
            msg='cancel_order {0} - {1}: status: {2} - {3}'.format(orderid,
                                                                   symbol,
                                                                   type(err),
                                                                   str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='cancel_order {0} - {1}: status: {2}'.format(orderid, symbol, status), level=logging.INFO)
        return status


def buy_order(symbol, amount, type_order, price_limit=0, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        if type_order == 'market':
            status = exchange.create_market_buy_order(symbol=symbol, amount=amount, params=params)
        elif type_order == 'limit':
            status = exchange.create_limit_buy_order(symbol=symbol, amount=amount, price=price_limit, params=params)
        else:
            raise Exception('ERROR: Type (market or limit)')
    except Exception as err:
        logger.log(
            msg='buy_order {0} - {1} - {2} ({3}): status: {4} - {5}'.format(type_order,
                                                                            symbol,
                                                                            amount,
                                                                            price_limit,
                                                                            type(err),
                                                                            str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='buy_order {0} - {1} - {2} ({3}): status: {4}'.format(type_order,
                                                                             symbol,
                                                                             amount,
                                                                             price_limit,
                                                                             status),
                   level=logging.INFO)
        return status


def sell_order(symbol, amount, type_order, price_limit=0, user=None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        if type == 'market':
            status = exchange.create_market_sell_order(symbol=symbol, amount=amount, params=params)
        elif type == 'limit':
            status = exchange.create_limit_sell_order(symbol=symbol, amount=amount, price=price_limit, params=params)
        else:
            raise Exception('ERROR: Type (market or limit)')
    except Exception as err:
        logger.log(
            msg='sell_order {0} - {1} - {2} ({3}): status: {4} - {5}'.format(type_order,
                                                                             symbol,
                                                                             amount,
                                                                             price_limit,
                                                                             type(err),
                                                                             str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='sell_order {0} - {1} - {2} ({3}): status: {4}'.format(type_order,
                                                                              symbol,
                                                                              amount,
                                                                              price_limit,
                                                                              status),
                   level=logging.INFO)
        return status
