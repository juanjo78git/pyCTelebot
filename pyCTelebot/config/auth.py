# -*- coding: utf-8 -*-
import os

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
