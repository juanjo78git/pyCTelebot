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


def strategies_symbol_list():
    my_strategy_symbols = []
    try:
        logger.log(msg='strategies_symbol_list: Start', level=logging.DEBUG)
        query = 'select * from strategy_symbols '
        args = []
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        for strategy_symbols in result:
            my_strategy_symbols.append(dict(strategy_symbols))
    except Exception as err:
        logger.log(msg='strategies_symbol_list: {0}'.format(str(err)), level=logging.ERROR)
    return my_strategy_symbols
