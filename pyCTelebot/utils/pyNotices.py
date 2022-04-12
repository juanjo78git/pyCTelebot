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


def run():
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='Notices start ID: {0}'.format(seed), level=logging.INFO)
    # Do something
    users = user_list()
    logger.log(msg='Notices users: {0}'.format(users), level=logging.DEBUG)
    for user in users:
        logger.log(msg='Notices user: {0}'.format(user), level=logging.DEBUG)
        bal = pyCrypto.balance(user_id=user.get('user_id'))
        logger.log(msg='Notices balance: {0}'.format(bal), level=logging.DEBUG)
        pyTelegram.private_message(user=user,
                                   message=_('Your Balance at {0} is: {1}').format(
                                       datetime.now(tz=pytz.timezone("Europe/Madrid")),
                                       bal
                                   ))
    logger.log(msg='Notices stop ID: {0}'.format(seed), level=logging.INFO)
