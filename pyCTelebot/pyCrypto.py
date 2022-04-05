# -*- coding: utf-8 -*-

from ccxt import binance, kucoin
from pyCTelebot.config.auth import TOKEN_CRYPTO_KEY_RO, TOKEN_CRYPTO_SECRET_RO, ENV_CONFIG, select_user
import gettext
import logging

# i18n
_ = gettext.gettext

# TODO: Test Exchange
if ENV_CONFIG.get('env') != 'TEST':
    params = {}
else:
    params = {'test': True}

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


def connection(user: str = 'ME'):
    # Binance connection
    logger.log(msg='Exchange connection user: {0}'.format(user), level=logging.DEBUG)
    exchange = None
    try:
        if user == 'READONLY':
            exchange = binance({
                'apiKey': TOKEN_CRYPTO_KEY_RO,
                'secret': TOKEN_CRYPTO_SECRET_RO
            })
        else:
            u = select_user(user=user, telegram_id=user)
            if u is None:
                raise Exception("User does not exist {0}".format(user))
            if u['exchange'] == 'binance':
                exchange = binance({
                    'apiKey': u['apiKey'],
                    'secret': u['secret']
                })
            elif u['exchange'] == 'kucoin':
                exchange = kucoin({
                    'apiKey': u['apiKey'],
                    'secret': u['secret'],
                    'password': u['passphrase']
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


def price(symbol: str, user: str = None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        """
        NOTE: period is 24h
        ticker = {
            'symbol':        string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
            'info':        { the original non-modified un-parsed reply from exchange API },
            'timestamp':     int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
            'datetime':      ISO8601 datetime string with milliseconds
            'high':          float, // highest price
            'low':           float, // lowest price
            'bid':           float, // current best bid (buy) price
            'bidVolume':     float, // current best bid (buy) amount (may be missing or undefined)
            'ask':           float, // current best ask (sell) price
            'askVolume':     float, // current best ask (sell) amount (may be missing or undefined)
            'vwap':          float, // volume weighed average price
            'open':          float, // opening price
            'close':         float, // price of last trade (closing price for current period)
            'last':          float, // same as `close`, duplicated for convenience
            'previousClose': float, // closing price for the previous period
            'change':        float, // absolute change, `last - open`
            'percentage':    float, // relative change, `(change/open) * 100`
            'average':       float, // average price, `(last + open) / 2`
            'baseVolume':    float, // volume of base currency traded for last 24 hours
            'quoteVolume':   float, // volume of quote currency traded for last 24 hours
        }
        """
        # without params=params
        ticker = exchange.fetch_ticker(symbol=symbol)
        logger.log(msg='Search price {0} --> value: {1}'.format(symbol, ticker), level=logging.DEBUG)

    except Exception as err:
        logger.log(
            msg='price {0}: status: {1} - {2}'.format(symbol,
                                                      type(err),
                                                      str(err)),
            level=logging.ERROR)
        raise
    else:
        return ticker


def open_orders(symbol: str, user: str = None):
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
        logger.log(msg='Open orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.DEBUG)
        return orders


def closed_orders(symbol: str, user: str = None):
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
        logger.log(msg='Closed orders: symbol {0} - Count: {1}'.format(symbol, len(orders)), level=logging.DEBUG)
        return orders


def balance(symbol: str = None, user: str = None):
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
            logger.log(msg='All balances:  {0}'.format(all_balances), level=logging.DEBUG)
            return all_balances
        else:
            logger.log(msg='Balance: symbol {0} - Value: {1}'.format(symbol, balances[symbol]), level=logging.DEBUG)
            return balances[symbol]


def cancel_order(order_id: str, symbol: str, user: str = None):
    if user is None:
        exchange = connection(user='READONLY')
    else:
        exchange = connection(user=user)
    try:
        status = exchange.cancel_order(id=order_id, symbol=symbol, params=params)
    except Exception as err:
        # Like OrderNotFound exception
        logger.log(
            msg='cancel_order {0} - {1}: status: {2} - {3}'.format(order_id,
                                                                   symbol,
                                                                   type(err),
                                                                   str(err)),
            level=logging.ERROR)
        raise
    else:
        logger.log(msg='cancel_order {0} - {1}: status: {2}'.format(order_id, symbol, status), level=logging.DEBUG)
        return status


def buy_order(symbol: str, amount, type_order: str, price_limit=0, user: str = None):
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
                   level=logging.DEBUG)
        return status


def sell_order(symbol: str, amount, type_order: str, price_limit=0, user: str = None):
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
                   level=logging.DEBUG)
        return status
