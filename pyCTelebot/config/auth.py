# -*- coding: utf-8 -*-
import os

# Token bot telegram
# TOKEN_TELEGRAM = 'Your Token'
TOKEN_TELEGRAM = os.environ["TOKEN_TELEGRAM"]

# Webook telegram Heroku
WEBHOOK_URL_TELEGRAM = 'https://pyctelebot.herokuapp.com/'
PORT = int(os.environ.get('PORT', 5000))

# API crypto info
TOKEN_CRYPTO_KEY = os.environ["TOKEN_CRYPTO_KEY"]
TOKEN_CRYPTO_SECRET = os.environ["TOKEN_CRYPTO_SECRET"]

# USER_ADMIN = 'USER_ID_TELEGRAM'
USER_ADMIN = os.environ["USER_ADMIN"]
