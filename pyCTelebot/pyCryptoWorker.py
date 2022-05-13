# -*- coding: utf-8 -*-

from pyCTelebot.utils import pyTelegram
from datetime import datetime
import gettext
import logging
from pyCTelebot.config.pyVars import ENV_CONFIG
import pytz
import random
import sys
# i18n
from pyCTelebot.utils.pyPrices import update_price_info

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
    """ Worker """
    seed = random.randint(0, sys.maxsize)
    logger.log(msg='Worker start ID: {0}'.format(seed), level=logging.INFO)
    # pyTelegram.message_admins(message='Worker start at {0} with ID: {1}'.format(
    #     datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))
    try:
        # Update price info
        update_price_info()
        # TODO: Update strategy info

    except Exception as err:
        logger.log(msg='Worker stop/KILLED ID: {0} - {1}'.format(seed, str(err)), level=logging.ERROR)
        pyTelegram.message_admins(message='Worker stop/KILLED at {0} with ID: {1}'.format(
            datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))
    else:
        logger.log(msg='Worker stop ID: {0}'.format(seed), level=logging.INFO)
        # pyTelegram.message_admins(message='Worker stop at {0} with ID: {1}'.format(
        #     datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))
