# -*- coding: utf-8 -*-

import gettext
import logging
# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
from pyCTelebot import pyCryptoWorker

# i18n
_ = gettext.gettext

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    logger.log(msg='CryptoCron start!', level=logging.INFO)
    # Mute log
    logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
    logging.getLogger('apscheduler.scheduler').propagate = False
    # Create an instance of scheduler and add function.
    scheduler = BlockingScheduler()
    scheduler.add_job(pyCryptoWorker.run, "interval", seconds=10)

    scheduler.start()
