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


# strategy_symbols table:
#   strategy_id VARCHAR(50)
#   exchange VARCHAR(50)
#   symbol VARCHAR(50)
#   unit_value NUMERIC
#   take_profit NUMERIC
#   buy_in_callback NUMERIC
def strategy_symbols_list(strategy_id: str = None,
                          exchange: str = None,
                          symbol: str = None):
    my_strategy_symbols = []
    try:
        logger.log(msg='strategy_symbols_list: Start {0}'.format(strategy_id), level=logging.DEBUG)
        query = 'select * from strategy_symbols '
        args = []
        query += ' where 1=1 '
        if strategy_id is not None:
            query += ' and strategy_id = %s '
            args.append(strategy_id)
        if exchange is not None:
            query += ' and exchange = %s '
            args.append(exchange)
        if symbol is not None:
            query += ' and symbol = %s '
            args.append(symbol)
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        for strategy_symbols in result:
            my_strategy_symbols.append(dict(strategy_symbols))
    except Exception as err:
        logger.log(msg='strategy_symbols_list: {0}'.format(str(err)), level=logging.ERROR)
    return my_strategy_symbols


# strategy_steps table:
#   strategy_id VARCHAR(50)
#   exchange VARCHAR(50)
#   symbol VARCHAR(50)
#   step INTEGER
#   step_type VARCHAR(50)
#   margin NUMERIC
#   units NUMERIC
def strategy_steps_list(strategy_id: str = None,
                        exchange: str = None,
                        symbol: str = None):
    my_strategy_symbols = []
    try:
        logger.log(msg='strategy_steps_list: Start {0}'.format(strategy_id), level=logging.DEBUG)
        query = 'select * from strategy_steps '
        args = []
        query += ' where 1=1 '
        if strategy_id is not None:
            query += ' and strategy_id = %s '
            args.append(strategy_id)
        if exchange is not None:
            query += ' and exchange = %s '
            args.append(exchange)
        if symbol is not None:
            query += ' and symbol = %s '
            args.append(symbol)
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        for strategy_symbols in result:
            my_strategy_symbols.append(dict(strategy_symbols))
    except Exception as err:
        logger.log(msg='strategy_steps_list: {0}'.format(str(err)), level=logging.ERROR)
    return my_strategy_symbols
