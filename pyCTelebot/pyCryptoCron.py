# -*- coding: utf-8 -*-

import gettext
import logging
# Package Scheduler.
import os
import random
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from pyCTelebot import pyCryptoWorker, pyTelegram
from pyCTelebot.config.auth import ENV_CONFIG

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

    logger.log(msg='CryptoCron start! ID: {0}'.format(seed), level=logging.INFO)
    pyTelegram.message_admins(message='CryptoCron start ID: {0}'.format(seed))

    # Mute log
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.scheduler').propagate = False

    # Create an instance of scheduler and add function.
    scheduler = BlockingScheduler()
    scheduler.add_job(pyCryptoWorker.run, "interval", seconds=60)
    s = int(os.environ.get('PERIOD_TEST', '520')) + 5
    scheduler.add_job(pyCryptoWorker.alert_worker, "interval", seconds=s)

    scheduler.start()
    logger.log(msg='CryptoCron stop! ID: {0}'.format(seed), level=logging.INFO)
    pyTelegram.message_admins(message='CryptoCron stop ID: {0}'.format(seed))
