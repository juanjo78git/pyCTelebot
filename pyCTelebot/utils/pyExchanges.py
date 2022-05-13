# -*- coding: utf-8 -*-

from pyCTelebot.config.pyVars import ENV_CONFIG
import gettext
import logging
from pyCTelebot.utils.pyDB import MyDB

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


def exchange_connection(exchange: str):
    """ exchange connection """
    try:
        logger.log(msg='exchange_connection - exchange: {0}'.format(exchange),
                   level=logging.DEBUG)
        query = "select * from exchanges where exchange = %s "
        args = [exchange]
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        if len(result) == 1:
            return dict(result[0])
    except Exception as err:
        logger.log(msg='exchange_connection: {0}'.format(str(err)), level=logging.ERROR)
    return None
