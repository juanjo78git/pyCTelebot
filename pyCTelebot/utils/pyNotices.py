# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
import pytz
from datetime import datetime

from pyCTelebot.utils import pyTelegram, pyCrypto
from pyCTelebot.config.pyVars import ENV_CONFIG

# i18n
from pyCTelebot.utils.pyUsers import user_list

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


def run2():
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='Notices start ID: {0}'.format(seed), level=logging.INFO)
    # Do something
    users = user_list()
    logger.log(msg='Notices users: {0}'.format(users), level=logging.DEBUG)
    for user in users:
        logger.log(msg='Notices user: {0}'.format(user.get('user_id')), level=logging.DEBUG)
        bal = pyCrypto.balance(user_id=user.get('user_id'))
        pyTelegram.private_message(user=user,
                                   message=_('Your Balance at {0} is: {1}').format(
                                       datetime.now(tz=pytz.timezone("Europe/Madrid")),
                                       bal
                                   ))
    logger.log(msg='Notices stop ID: {0}'.format(seed), level=logging.INFO)


def run():
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='Notices start ID: {0}'.format(seed), level=logging.INFO)
    # Do something
    users = user_list()
    logger.log(msg='Notices users: {0}'.format(users), level=logging.DEBUG)
    for user in users:
        logger.log(msg='Notices user: {0}'.format(user.get('user_id')), level=logging.DEBUG)

        bal = pyCrypto.mybalance(user_id=user.get('user_id'))
        # Los mensajes deberian estar en una plantilla y solo hacer las sustituciones
        body = '{0:<6} {1:<11} {2:>10}\n'.format('Crypto', 'Cantidad', 'Balance')
        body += '------------------------------\n'
        for index, row in bal[['Altname', 'Balance', 'Precio', 'dBalance']].sort_values(by=['dBalance'],
                                                                                        ascending=False).iterrows():
            body += '{0:<6} {1:<12} {2:>10}\n'.format(row['Altname'], row['Balance'], row['dBalance'])

        body += '------------------------------\n'
        body += 'Total ⇉ {0}\n'.format(bal['dBalance'].sum())
        logger.log(msg=body, level=logging.DEBUG)
        pyTelegram.message_admins(message=body)

    logger.log(msg='Notices stop ID: {0}'.format(seed), level=logging.INFO)
