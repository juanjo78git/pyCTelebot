# -*- coding: utf-8 -*-
import os
import gettext
import logging
import json

# i18n
_ = gettext.gettext
# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Token bot telegram
# TOKEN_TELEGRAM = 'Your Token'
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM', 'NOT_FOUND')

# Webhook telegram Heroku
WEBHOOK_URL_TELEGRAM = 'https://pyctelebot.herokuapp.com/'
PORT = int(os.environ.get('PORT', 5000))

# API crypto info
TOKEN_CRYPTO_KEY = os.environ.get('TOKEN_CRYPTO_KEY', 'NOT_FOUND')
TOKEN_CRYPTO_SECRET = os.environ.get('TOKEN_CRYPTO_SECRET', 'NOT_FOUND')

# API crypto info Read-only
TOKEN_CRYPTO_KEY_RO = os.environ.get('TOKEN_CRYPTO_KEY_RO', TOKEN_CRYPTO_KEY)
TOKEN_CRYPTO_SECRET_RO = os.environ.get('TOKEN_CRYPTO_SECRET_RO', TOKEN_CRYPTO_SECRET)

# USER_ADMIN = 'USER_ID_TELEGRAM'
USER_ADMIN = os.environ.get('USER_ADMIN', '[0]').strip('[]').replace(' ', '').split(',')

USER_LIST = json.loads(os.environ.get('USER_LIST', '[]'))


def users(role='ALL'):
    my_users = []
    for user in USER_LIST:
        if user['role'] == role or role == 'ALL':
            my_users.append(user)
    return my_users


def select_user(user=None, telegramid=None):
    if user is not None or telegramid is not None:
        for my_user in USER_LIST:
            if my_user['user'] == user or my_user['telegramid'] == str(telegramid):
                return my_user
    return None
