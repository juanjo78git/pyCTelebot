# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
from telegram import Update
from telegram.ext import CallbackContext
from pyCTelebot.config.pyVars import ENV_CONFIG, POC_MAX_PRICE, POC_MIN_PRICE, POC_USER

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
    used_coin = 'LUNA'
    used_stable_coin = 'USDT'
    used_symbol = used_coin + '/' + used_stable_coin
    max_price = POC_MAX_PRICE
    min_price = POC_MIN_PRICE
    my_user_id = POC_USER
    if my_user_id is None:
        return 1
    my_user = pyUsers.select_user(user_id=my_user_id)
    pyTelegram.private_message(message='PARTY!! {0}\n Max: {1}\n Min: {2}'.format(used_symbol, max_price, min_price),
                               user=my_user)
    exchange = pyCrypto.MyCrypto(exchange_name='kucoin', user_id=my_user_id)
    my_open_order = exchange.open_orders(symbol=used_symbol)
    my_balance = exchange.balance(used_coin)
    my_balance_coin = 0
    my_balance_stable_coin = 0
    if len(my_balance) > 0:
        my_balance_coin = my_balance[0].get('amount')
    my_balance_stable = exchange.balance(used_stable_coin)
    if len(my_balance_stable) > 0:
        my_balance_stable_coin = my_balance_stable[0].get('amount')

    print(my_open_order[0].get('side'))
    print(my_balance_stable)
    # No tengo ordenes abiertas
    if len(my_open_order) == 0:
        # Tengo las crypto compradas
        if my_balance_coin > 0:
            # ORDEN DE VENTA (LIMIT) A MAXIMO
            pyTelegram.private_message(message='I have:\n {0} {1}'.format(used_coin, my_balance_coin),
                                       user=my_user)

            print('I have: {0} {1}'.format(used_coin, my_balance_coin))
            try:
                exchange.sell_order(symbol=used_symbol, amount=my_balance_coin,
                                    type_order='limit', price_limit=max_price)
            except Exception as err:
                pyTelegram.private_message(message='Error SELL ORDER:\n {0}'.format(err),
                                           user=my_user)
        # Lo tengo en stable coin (el 1 es por los restos y el 50 )
        elif 1 < my_balance_stable_coin < 50:
            # ORDEN DE COMPRA (LIMIT) A MINIMO
            print('I have: {0} {1}'.format(used_stable_coin, my_balance_stable_coin))
            pyTelegram.private_message(message='I have:\n {0} {1}'.format(used_coin, my_balance_coin),
                                       user=my_user)
            try:
                exchange.buy_order(symbol=used_symbol, amount=my_balance_stable_coin, type_order='limit',
                                   price_limit=min_price)
            except Exception as err:
                pyTelegram.private_message(message='Error BUY ORDER:\n {0}'.format(err),
                                           user=my_user)
        else:
            pyTelegram.private_message(message='I have:\n {0} {1} \n {2} {3}'.format(used_coin,
                                                                                     my_balance_coin,
                                                                                     used_stable_coin,
                                                                                     my_balance_stable_coin),
                                       user=my_user)
    # Ya tengo ordenes abiertas y preparadas
    else:
        # No hago nada
        pyTelegram.private_message(message='I have:\n {0} {1} \n {2} {3} \n '
                                           'Orders: \n {4}'.format(used_coin,
                                                                   my_balance_coin,
                                                                   used_stable_coin,
                                                                   my_balance_stable_coin,
                                                                   pyTemplates.templates_json(my_open_order)),
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
    logger.log(msg='any_message_poc telegram_id: {0} name: {1} ({2}) '
                   'message: {3}'.format(update.effective_user.id,
                                         update.effective_user.name,
                                         update.effective_user.full_name,
                                         update.effective_message.text),
               level=logging.INFO)
