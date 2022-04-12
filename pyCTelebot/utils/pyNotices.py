# -*- coding: utf-8 -*-

import gettext
import logging
import random
import sys
import pytz
from datetime import datetime

from pyCTelebot.utils import pyTelegram
from pyCTelebot.config.pyVars import ENV_CONFIG

# i18n
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
    pyTelegram.message_admins(message='Notices: HELLO!!! at {0} with ID: {1}'.format(
        datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))

    logger.log(msg='Notices stop ID: {0}'.format(seed), level=logging.INFO)
