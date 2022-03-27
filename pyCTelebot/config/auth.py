# -*- coding: utf-8 -*-
import os

# Token bot telegram
# TOKEN_TELEGRAM = 'Your Token'
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM', 'NOT_FOUND')

# Webook telegram Heroku
WEBHOOK_URL_TELEGRAM = 'https://pyctelebot.herokuapp.com/'
PORT = int(os.environ.get('PORT', 5000))

# API crypto info
TOKEN_CRYPTO_KEY = os.environ.get('TOKEN_CRYPTO_KEY', 'NOT_FOUND')
TOKEN_CRYPTO_SECRET = os.environ.get('TOKEN_CRYPTO_SECRET', 'NOT_FOUND')

# USER_ADMIN = 'USER_ID_TELEGRAM'
USER_ADMIN = os.environ.get('USER_ADMIN', '[0]').strip('[]').replace(' ', '').split(',')
