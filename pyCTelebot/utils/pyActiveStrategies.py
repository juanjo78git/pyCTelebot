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


# active_strategy_symbols table:
#   user_id VARCHAR(50)
#   strategy_id VARCHAR(50)
#   exchange VARCHAR(50)
#   symbol VARCHAR(50)
#   unit_value NUMERIC
#   take_profit NUMERIC
#   user_id VARCHAR(50)
# 	strategy_id VARCHAR(50)
# 	exchange VARCHAR(50)
# 	symbol VARCHAR(50)
# 	unit_value NUMERIC
# 	take_profit NUMERIC
# 	status VARCHAR(50)
# 	current_invest NUMERIC
# 	current_profit NUMERIC
# 	start_audit_date TIMESTAMP
# 	end_audit_date TIMESTAMP
def active_strategy_symbols_list(user_id: str = None,
                                 strategy_id: str = None,
                                 exchange: str = None,
                                 symbol: str = None):
    my_strategy_symbols = []
    try:
        logger.log(msg='active_strategy_symbols_list: Start {0}'.format(strategy_id), level=logging.DEBUG)
        query = 'select * from active_strategy_symbols '
        args = []
        if strategy_id is not None or user_id is not None or exchange is not None or symbol is not None:
            query += ' where 1=1 '
        if strategy_id is not None:
            query += ' and strategy_id = %s '
            args.append(strategy_id)
        if user_id is not None:
            query += ' and user_id = %s '
            args.append(user_id)
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
        logger.log(msg='active_strategy_symbols_list: {0}'.format(str(err)), level=logging.ERROR)
    return my_strategy_symbols
