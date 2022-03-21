# -*- coding: utf-8 -*-
import os

# Token bot telegram
# TOKEN_TELEGRAM = 'Your Token'
TOKEN_TELEGRAM = os.environ["TOKEN_TELEGRAM"]

# Webook telegram Heroku
WEBHOOK_URL_TELEGRAM = 'https://pyctelebot.herokuapp.com/'
PORT = int(os.environ.get('PORT', 5000))

# Token crypto info
# TOKEN_CRYPTO = 'Your Token'
TOKEN_CRYPTO = os.environ["TOKEN_CRYPTO"]
