# -*- coding: utf-8 -*-

from ccxt import binance, kucoin, kraken
from pyCTelebot.config.pyVars import ENV_CONFIG
from pyCTelebot.utils.pyExchanges import exchange_connection
from pyCTelebot.utils.pyUsers import select_user, select_user_exchanges, decrypt
import gettext
import logging

# i18n
_ = gettext.gettext

# TODO: Test Exchange
# if ENV_CONFIG.get('env') != 'TEST':
params = {}
# else:
#    params = {'test': True}

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


class MyCrypto:
    default_stable_coin = 'USDT'
    default_stable_coin2 = 'EUR'
    exchange = None
    user = None

    def __init__(self, exchange_name: str, user_id: str = None, telegram_id: str = None):
        if user_id is None and telegram_id is None:
            user = exchange_connection(exchange=exchange_name)
        else:
            user = select_user(user_id=user_id, telegram_id=telegram_id, exchange=exchange_name)
        if user is None:
            raise Exception(
                "User/exchange does not exist {0} - {1} - {2}".format(user_id, telegram_id, exchange_name))
        self.connection(exchange_name=exchange_name, user=user)

    def connection(self, exchange_name: str, user=None):
        # Binance connection
        logger.log(msg='Exchange connection user: {0}'.format(exchange_name), level=logging.DEBUG)
        self.exchange = None
        try:
            if user is None:
                user = exchange_connection(exchange=exchange_name)
                if user is None:
                    raise Exception(
                        "User/exchange does not exist {0} - {1}".format(user, exchange_name))
            if user['exchange'] == 'binance':
                self.exchange = binance({
                    'apiKey': decrypt(user['apikey']),
                    'secret': decrypt(user['secret'])
                })
            elif user['exchange'] == 'kucoin':
                self.exchange = kucoin({
                    'apiKey': decrypt(user['apikey']),
                    'secret': decrypt(user['secret']),
                    'password': decrypt(user['passphrase'])
                })
            elif user['exchange'] == 'kraken':
                self.exchange = kraken({
                    'apiKey': decrypt(user['apikey']),
                    'secret': decrypt(user['secret'])
                })
            # enable rate limiting
            # exchange.enableRateLimit = True
        except Exception as err:
            logger.log(msg='connection: status: {0} - {1}'.format(type(err), str(err)), level=logging.ERROR)
            raise

    def price(self, symbol: str):
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
            ticker = self.exchange.fetch_ticker(symbol=symbol)
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

    def open_orders(self, symbol: str):
        try:
            orders = self.exchange.fetch_open_orders(symbol=symbol, params=params)
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

    def closed_orders(self, symbol: str):
        try:
            orders = self.exchange.fetch_closed_orders(symbol=symbol, params=params)
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

    def balance(self, symbol: str = None):
        try:

            balances = self.exchange.fetch_total_balance(params=params)

            all_balances = []
            for key in balances:
                if balances[key] != 0:
                    if symbol is None or symbol == key:
                        key_conversion_value_stable_coin = 0
                        key_conversion_value_stable_coin2 = 0
                        try:
                            if key == self.default_stable_coin:
                                key_conversion_value_stable_coin = balances[key]
                            else:
                                stable_coin_price = self.price(symbol=key + '/' + self.default_stable_coin)['ask']
                                key_conversion_value_stable_coin = balances[key] * stable_coin_price
                        except Exception as err:
                            logger.log(
                                msg='balance {0}: status: {1} - {2}'.format(symbol,
                                                                            type(err),
                                                                            str(err)),
                                level=logging.ERROR)
                        try:
                            if key == self.default_stable_coin2:
                                key_conversion_value_stable_coin2 = balances[key]
                            else:
                                stable_coin2_price = self.price(symbol=key + '/' + self.default_stable_coin2)['ask']
                                key_conversion_value_stable_coin2 = balances[key] * stable_coin2_price
                        except Exception as err:
                            logger.log(
                                msg='balance {0}: status: {1} - {2}'.format(symbol,
                                                                            type(err),
                                                                            str(err)),
                                level=logging.ERROR)
                        all_balances.append({
                            'exchange': self.exchange.name,
                            'currency': key,
                            'amount': balances[key],
                            self.default_stable_coin: key_conversion_value_stable_coin,
                            self.default_stable_coin2: key_conversion_value_stable_coin2
                        })
        except Exception as err:
            logger.log(
                msg='balance {0}: status: {1} - {2}'.format(symbol,
                                                            type(err),
                                                            str(err)),
                level=logging.ERROR)
            raise
        else:
            logger.log(msg='All balances:  {0}'.format(all_balances), level=logging.DEBUG)
            return all_balances

    def cancel_order(self, order_id: str, symbol: str):
        try:
            status = self.exchange.cancel_order(id=order_id, symbol=symbol, params=params)
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

    def buy_order(self, symbol: str, amount, type_order: str, price_limit=0):
        try:
            if type_order == 'market':
                status = self.exchange.create_market_buy_order(symbol=symbol, amount=amount, params=params)
            elif type_order == 'limit':
                status = self.exchange.create_limit_buy_order(symbol=symbol, amount=amount, price=price_limit,
                                                              params=params)
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

    def sell_order(self, symbol: str, amount, type_order: str, price_limit=0):
        try:
            if type_order == 'market':
                status = self.exchange.create_market_sell_order(symbol=symbol, amount=amount, params=params)
            elif type_order == 'limit':
                status = self.exchange.create_limit_sell_order(symbol=symbol, amount=amount, price=price_limit,
                                                               params=params)
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


# TODO: refactor, no here
def balance_all_exchanges(symbol: str = None, user_id: str = None, telegram_id: str = None):
    if user_id is None:
        u = select_user(user_id=user_id, telegram_id=telegram_id)
        if u is None:
            return {}
        user_id = u['user_id']
    user_exchanges = select_user_exchanges(user_id=user_id)
    all_balances = []
    for e in user_exchanges:
        exchange = MyCrypto(exchange_name=e['exchange'], user_id=user_id)
        all_balances.extend(exchange.balance(symbol=symbol))
    return all_balances
