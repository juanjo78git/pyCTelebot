# -*- coding: utf-8 -*-

import gettext
import logging
# Package Scheduler.
import random
import sys
import pytz
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from pyCTelebot import pyCryptoWorker
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

    logger.log(msg='CryptoCron start ID: {0}'.format(seed), level=logging.INFO)
    pyTelegram.message_admins(message='CryptoCron start at {0} with ID: {1}'.format(
        datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))

    # Mute log
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.scheduler').propagate = False

    # Create an instance of scheduler and add function.
    scheduler = BlockingScheduler()
    scheduler.add_job(pyCryptoWorker.run, "interval", seconds=3)
    try:
        scheduler.start()
    finally:
        logger.log(msg='CryptoCron stop ID: {0}'.format(seed), level=logging.INFO)
        pyTelegram.message_admins(message='CryptoCron stop  at {0} with ID: {1}'.format(
            datetime.now(tz=pytz.timezone("Europe/Madrid")), seed))
