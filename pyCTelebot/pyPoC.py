# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext
from pyCTelebot.config.pyVars import ENV_CONFIG, POC_MAX_PRICE, POC_MIN_PRICE, POC_USER, POC_COIN, \
    POC_PROFIT_STABLE_COIN

# i18n
from pyCTelebot.utils import pyPrices, pyTemplates, pyCrypto, pyTelegram, pyUsers

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
# Force DEBUG
logger.setLevel(logging.DEBUG)


def run():
    """ Proof of Concept """
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run start ID: {0}'.format(seed), level=logging.INFO)
    # Do something
    used_coin = POC_COIN
    used_stable_coin = 'USDT'
    used_symbol = used_coin + '/' + used_stable_coin
    max_price = POC_MAX_PRICE
    min_price = POC_MIN_PRICE
    my_user_id = POC_USER
    profit_stable_coin = POC_PROFIT_STABLE_COIN
    if my_user_id is None:
        return 1
    my_user = pyUsers.select_user(user_id=my_user_id)
    exchange = pyCrypto.MyCrypto(exchange_name='kucoin', user_id=my_user_id)
    price_coin_temp = exchange.price(used_symbol)
    price_coin_message = {
        'ask': price_coin_temp.get('ask', 'None'),
        'bid': price_coin_temp.get('bid', 'None'),
    }
    pyTelegram.private_message(message='PARTY!! {0}\n Max: {1}\n Min: {2}\n'
                                       'Current Price: {3}'.format(used_symbol,
                                                                   max_price,
                                                                   min_price,
                                                                   pyTemplates.templates_json(price_coin_message)),
                               user=my_user)
    my_open_order = exchange.open_orders(symbol=used_symbol)
    my_balance = exchange.balance(used_coin)
    my_balance_coin = 0.0
    my_balance_stable_coin = 0.0
    if len(my_balance) > 0:
        my_balance_coin = my_balance[0].get('amount')
    my_balance_stable = exchange.balance(used_stable_coin)
    if len(my_balance_stable) > 0:
        my_balance_stable_coin = my_balance_stable[0].get('amount')

    # I don't have open orders
    if len(my_open_order) == 0:
        # My balance is in crypto (residual crypto 0.001)
        if my_balance_coin > 0.001:
            logger.log(msg='pyPoC sell balance coin: {0}'.format(my_balance_coin), level=logging.INFO)
            # Sell order limit with max.
            status = None
            try:
                status = exchange.sell_order(symbol=used_symbol, amount=my_balance_coin,
                                             type_order='limit', price_limit=max_price)
            except Exception as err:
                logger.log(msg='ERROR: {0}'.format(err), level=logging.ERROR)
                pyTelegram.private_message(message='Error SELL ORDER:\n {0}'.format(err),
                                           user=my_user)
            pyTelegram.private_message(message='I have:\n {0} {1} \n Status: {2}'.format(used_coin,
                                                                                         my_balance_coin,
                                                                                         status),
                                       user=my_user)
        # My balance is in stable coin ( More than 1 and stop in 50 profit )
        elif 1 < my_balance_stable_coin < profit_stable_coin:
            logger.log(msg='pyPoC buy balance coin: {0}'.format(my_balance_stable_coin), level=logging.INFO)
            # Buy order limit with min.
            status = None
            pyTelegram.private_message(message='I have:\n {0} {1}'.format(used_coin, my_balance_coin),
                                       user=my_user)
            try:
                amount = int(my_balance_stable_coin) / min_price
                logger.log(msg='pyPoC buy balance: {0} - {1} - {2} - {3}'.format(used_symbol,
                                                                                 my_balance_stable_coin,
                                                                                 min_price,
                                                                                 amount),
                           level=logging.INFO)

                status = exchange.buy_order(symbol=used_symbol,
                                            amount=amount,
                                            type_order='limit',
                                            price_limit=min_price)
            except Exception as err:
                logger.log(msg='ERROR: {0}'.format(err), level=logging.ERROR)
                pyTelegram.private_message(message='Error BUY ORDER:\n {0}'.format(err),
                                           user=my_user)
            pyTelegram.private_message(message='I have:\n {0} {1} \n Status {2}'.format(used_coin,
                                                                                        my_balance_coin,
                                                                                        status),
                                       user=my_user)
        else:
            pyTelegram.private_message(message='I have:\n {0} {1} \n {2} {3}'.format(used_coin,
                                                                                     my_balance_coin,
                                                                                     used_stable_coin,
                                                                                     my_balance_stable_coin),
                                       user=my_user)
    # I have open orders
    else:
        # Nothing, only info
        logger.log(msg='pyPoC Nothing: {0}'.format(my_open_order), level=logging.INFO)

        my_open_order_message = []
        for order in my_open_order:
            my_open_order_message.append({
                'symbol': order.get('symbol', 'None'),
                'side': order.get('side', 'None'),
                'type': order.get('type', 'None'),
                'price': order.get('price', 'None'),
                'amount': order.get('amount', 'None'),
                'datetime': order.get('datetime', 'None'),
            })
        pyTelegram.private_message(message='I have:\n {0} {1} \n {2} {3} \n '
                                           'Orders: {4}'.format(used_coin,
                                                                my_balance_coin,
                                                                used_stable_coin,
                                                                my_balance_stable_coin,
                                                                pyTemplates.templates_json(my_open_order_message)),
                                   user=my_user)
    logger.log(msg='pyPoC run stop ID: {0}'.format(seed), level=logging.INFO)


def run_telegram(update: Update, context: CallbackContext):
    """ Telegram Proof of Concept """
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='pyPoC run_telegram start ID: {0}'.format(seed), level=logging.INFO)
    prices = pyPrices.price_info()
    for price in prices:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=_('{0} - {1}: \n'
                                        'Last buy: {2} \n'
                                        'Current buy: {3} \n'
                                        '{4} % \n'
                                        'Last sell: {5} \n'
                                        'Current sell: {6} \n'
                                        '{7} % \n'
                                        'Last date: {8} \n'
                                        'Current date: {9}').format(
                                     price.get('exchange'),
                                     price.get('symbol'),
                                     price.get('last_buy_price'),
                                     price.get('current_buy_price'),
                                     price.get('buy_price_variation_percentage'),
                                     price.get('last_sell_price'),
                                     price.get('current_sell_price'),
                                     price.get('sell_price_variation_percentage'),
                                     price.get('last_audit_date'),
                                     price.get('current_audit_date'),

                                 ))
    logger.log(msg='pyPoC run_telegram stop ID: {0}'.format(seed), level=logging.INFO)


def any_message_poc(update: Update, context: CallbackContext):
    """ Telegram Proof of Concept: any message do it! """
    logger.log(msg='pyPoC any_message_poc start', level=logging.INFO)
    # Do something
    logger.log(msg='any_message_poc telegram_id: {0} name: {1} ({2}) \n'
                   'message: {3}\n'
                   'bot ID: {4}'.format(update.effective_user.id,
                                        update.effective_user.name,
                                        update.effective_user.full_name,
                                        update.effective_message.text,
                                        context.bot.id),
               level=logging.INFO)
