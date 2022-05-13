# -*- coding: utf-8 -*-

from pyCTelebot.config.pyVars import ENV_CONFIG, ENCRYPTION_KEY
import gettext
import logging
from pyCTelebot.utils.pyDB import MyDB, convert
from cryptography.fernet import Fernet

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
#   "role": "USER/ADMIN"
# }
# user_exchanges table:
# { "user_id": "username",
#   "exchange": "Exchange name",
#   "apiKey": "Cryptocurrency exchange apiKey ",
#   "secret": "Cryptocurrency exchange secret",
#   "passphrase": "API Passphrase"
# }

def user_list(role: str = None):
    """ User list filtering by role in case this is passed as a parameter """
    my_users = []
    try:
        logger.log(msg='users - role: {0}'.format(role),
                   level=logging.DEBUG)
        query = 'select * from users '
        args = []
        if role is not None:
            query += ' where role = %s '
            args.append(role)
        db = MyDB()
        result = db.query(query=query, args=args)
        db.close()
        for user in result:
            my_users.append(dict(user))
    except Exception as err:
        logger.log(msg='users: {0}'.format(str(err)), level=logging.ERROR)
    return my_users


def select_user(user_id: str = None, telegram_id: str = None, exchange: str = None):
    """ Information of the indicated user, in case of passing exchange it also returns the info of this """
    try:
        logger.log(msg='select_user - user_id: {0} - telegram_id: {1} - exchange: {2}'.format(user_id,
                                                                                              telegram_id,
                                                                                              exchange),
                   level=logging.DEBUG)
        if user_id is not None or telegram_id is not None:
            query = 'SELECT u.user_id, u.telegram_id, u.email, u.role, ' \
                     ' e.exchange, e.apikey, e.secret, e.passphrase ' \
                    ' FROM users u ' \
                    ' LEFT JOIN user_exchanges e ' \
                    ' ON u.user_id = e.user_id ' \
                    ' WHERE 1=1 '
            args = []
            if user_id is not None:
                query += 'and u.user_id = %s '
                args.append(user_id)
            if telegram_id is not None:
                query += ' and u.telegram_id = %s '
                args.append(str(telegram_id))
            if exchange is not None:
                query += 'and e.exchange = %s '
                args.append(exchange)
            db = MyDB()
            result = db.query(query=query, args=args)
            db.close()
            # if len(result) == 1:
            return dict(result[0])
    except Exception as err:
        logger.log(msg='select_user: {0}'.format(str(err)), level=logging.ERROR)
    return None


def select_user_exchanges(user_id: str = None, exchange: str = None):
    """ Exchanges of the user indicated """
    my_user_exchanges = []
    try:
        logger.log(msg='select_user_exchanges - user_id: {0} - exchange: {1}'.format(user_id, exchange),
                   level=logging.DEBUG)
        if user_id is not None:
            query = 'SELECT e.exchange, e.apikey, e.secret, e.passphrase ' \
                    ' FROM user_exchanges e ' \
                    ' WHERE 1=1 '
            args = []
            if user_id is not None:
                query += 'and e.user_id = %s '
                args.append(user_id)
            if exchange is not None:
                query += 'and e.exchange = %s '
                args.append(exchange)
            db = MyDB()
            result = db.query(query=query, args=args)
            db.close()
            my_user_exchanges = convert(result)
    except Exception as err:
        logger.log(msg='select_user_exchanges: {0}'.format(str(err)), level=logging.ERROR)
    return my_user_exchanges


def authorization(user_id: str = None, telegram_id: str = None, action: str = None):
    """ Authorization """
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


# TODO: To encrypt a phrase
def encrypt(token: str, key=None):
    """ Encrypt a phrase """
    if key is not None:
        fernet = Fernet(key)
        return fernet.encrypt(token.encode())
    elif ENCRYPTION_KEY is not None:
        fernet = Fernet(bytes(ENCRYPTION_KEY, 'utf-8'))
        return fernet.encrypt(token.encode())
    else:
        return token


# TODO: To decrypt a phrase
def decrypt(token, key=None):
    """ Decrypt a phrase """
    if key is not None:
        fernet = Fernet(key)
        return fernet.decrypt(token).decode()
    elif ENCRYPTION_KEY is not None:
        fernet = Fernet(bytes(ENCRYPTION_KEY, 'utf-8'))
        return fernet.decrypt(token).decode()
    else:
        return token


# TODO: To get a new encryption key
def new_encryption_key(key: str = None):
    """ Get a new encryption key """
    if key is not None:
        return bytes(key, 'utf-8')
    else:
        return Fernet.generate_key()
