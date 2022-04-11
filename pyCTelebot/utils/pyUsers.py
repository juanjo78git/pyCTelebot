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


# users table:
# { "user_id": "username",
#   "telegram_id": "telegram ID",
#   "email": "email",
#   "role": "USER/ADMIN",
#   "exchange": "Exchange name",
#   "apiKey": "Cryptocurrency exchange apiKey ",
#   "secret": "Cryptocurrency exchange secret",
#   "passphrase": "API Passphrase"
# }
def user_list(role='ALL'):
    my_users = []
    try:
        logger.log(msg='users - role: {0}'.format(role),
                   level=logging.DEBUG)
        query = 'select * from users where '
        args = []
        query += " 'ALL' = %s or role = %s "
        print(query)
        args.append(role)
        args.append(role)
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        for user in result:
            my_users.append(dict(user))
    except Exception as err:
        logger.log(msg='users: {0}'.format(str(err)), level=logging.ERROR)
    return my_users


def select_user(user_id: str = None, telegram_id: str = None):
    try:
        logger.log(msg='select_user - user_id: {0} - telegram_id: {1}'.format(user_id, telegram_id),
                   level=logging.DEBUG)
        if user_id is not None or telegram_id is not None:
            query = 'select * from users where '
            args = []
            if user_id is not None:
                query += ' user_id = %s '
                args.append(user_id)
            if user_id is not None and telegram_id is not None:
                query += ' and '
            if telegram_id is not None:
                query += ' telegram_id = %s '
                args.append(str(telegram_id))
            db = MyDB()
            result = db.query(query=query, args=args)
            db.close()
            if len(result) == 1:
                return dict(result[0])
    except Exception as err:
        logger.log(msg='select_user: {0}'.format(str(err)), level=logging.ERROR)
    return None


def select_user_readonly(exchange: str):
    try:
        logger.log(msg='select_user_readonly - exchange: {0}'.format(exchange),
                   level=logging.DEBUG)
        query = "select * from users where "
        args = []
        query += " role = 'READ_ONLY' and "
        query += " exchange = %s "
        args.append(exchange)
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        if len(result) == 1:
            return dict(result[0])
    except Exception as err:
        logger.log(msg='select_user_readonly: {0}'.format(str(err)), level=logging.ERROR)
    return None


def authorization(user_id: str = None, telegram_id: str = None, action: str = None):
    logger.log(msg='authorization - User: {0} - {1} action: {2}'.format(user_id, telegram_id, action),
               level=logging.DEBUG)
    try:
        user = select_user(user_id=user_id, telegram_id=telegram_id)
        if user is None:
            return False
        elif user['role'] == 'ADMIN':
            return True
        elif user['role'] == 'USER' and action == 'message_admin':
            return True
        else:
            return False
    except Exception as err:
        logger.log(msg='authorization: {0}'.format(str(err)), level=logging.ERROR)
    return False
