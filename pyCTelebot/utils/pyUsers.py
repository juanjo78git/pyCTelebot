# -*- coding: utf-8 -*-

from pyCTelebot.config.pyVars import ENV_CONFIG, USER_LIST
import gettext
import logging

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


def users(role='ALL'):
    my_users = []
    for user in USER_LIST:
        if user['role'] == role or role == 'ALL':
            my_users.append(user)
    return my_users


def select_user(user_id=None, telegram_id=None):
    if user_id is not None or telegram_id is not None:
        for my_user in USER_LIST:
            if my_user['user'] == user_id or my_user['telegram_id'] == str(telegram_id):
                return my_user
    return None


def authorization(user_id: str = None, telegram_id=None, action: str = None):
    logger.log(msg='authorization - User: {0} - {1} action: {2}'.format(user_id, telegram_id, action),
               level=logging.DEBUG)
    try:
        if telegram_id is not None:
            if next((user for user in users('ADMIN') if user['telegram_id'] == str(telegram_id)), None):
                return True
            if (next((user for user in users('USER') if user['telegram_id'] == str(telegram_id)), None)) \
                    and action == 'message_admin':
                return True
            else:
                return False
        elif user_id is not None:
            if next((user for user in users('ADMIN') if user['user_id'] == str(user_id)), None):
                return True
            if (next((user for user in users('USER') if user['user_id'] == str(user_id)), None)) \
                    and action == 'message_admin':
                return True
            else:
                return False
        else:
            return False
    except Exception as err:
        logger.log(msg='authorization: {0}'.format(str(err)), level=logging.ERROR)
    return False
