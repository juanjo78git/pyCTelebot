# -*- coding: utf-8 -*-

import gettext
import logging
# Package Scheduler.
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from pyCTelebot import pyCryptoWorker
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
    s = int(os.environ.get('PERIOD_TEST', '5')) + 5
    logger.log(msg='CryptoCron start! {0} seconds'.format(s), level=logging.INFO)
    # Mute log
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.scheduler').propagate = False
    # Create an instance of scheduler and add function.
    scheduler = BlockingScheduler()
    scheduler.add_job(pyCryptoWorker.run, "interval", seconds=s)

    scheduler.start()
