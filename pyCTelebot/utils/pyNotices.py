# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
import pytz
from datetime import datetime

from pyCTelebot.utils import pyTelegram, pyCrypto, pyTemplates
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


def run():
    """ Send info about exchanges """
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='Notices start ID: {0}'.format(seed), level=logging.INFO)
    # Do something
    users = user_list()
    for user in users:
        logger.log(msg='Notices user: {0}'.format(user.get('user_id')), level=logging.DEBUG)
        bal = pyCrypto.balance_all_exchanges(user_id=user.get('user_id'))
        total_usdt = 0
        total_eur = 0
        for b in bal:
            total_usdt += b.get(pyCrypto.MyCrypto.default_stable_coin, 0)
            total_eur += b.get(pyCrypto.MyCrypto.default_stable_coin2, 0)

        pyTelegram.private_message(user=user,
                                   message=_('Your Balance at {0} is: {1} \n'
                                             'Total ' + pyCrypto.MyCrypto.default_stable_coin + ': {2} \n'
                                             'Total ' + pyCrypto.MyCrypto.default_stable_coin2 + ': {3}').format(
                                       datetime.now(tz=pytz.timezone("Europe/Madrid")),
                                       pyTemplates.templates_json(bal, 'all_balances'),
                                       total_usdt,
                                       total_eur
                                   ))
    logger.log(msg='Notices stop ID: {0}'.format(seed), level=logging.INFO)
