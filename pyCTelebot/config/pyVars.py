# -*- coding: utf-8 -*-
import os
import gettext
import logging
import json

# i18n
_ = gettext.gettext
# Logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Token bot telegram
# TOKEN_TELEGRAM = 'Your Token'
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM', 'NOT_FOUND')

# Webhook telegram Heroku
WEBHOOK_URL_TELEGRAM = 'https://pyctelebot.herokuapp.com/'
PORT = int(os.environ.get('PORT', 5000))

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', "NOT_FOUND")

# Environment config
# log values: DEBUG / INFO / WARNING / ERROR / CRITICAL
# env values: TEST / PROD
ENV_CONFIG = json.loads(os.environ.get('ENV_CONFIG', '{"log": "DEBUG", "env": "TEST"}'))

# Telegram admin group id list
TELEGRAM_ADMIN_GROUP = json.loads(os.environ.get('TELEGRAM_ADMIN_GROUP', "[]"))

# Encryption key
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', None)

# PoC
POC_COIN = os.environ.get('POC_COIN', 'LUNA')
POC_MAX_PRICE = os.environ.get('POC_MAX_PRICE', 0.0004)
POC_MIN_PRICE = os.environ.get('POC_MIN_PRICE', 0.00028)
POC_PROFIT_STABLE_COIN = os.environ.get('POC_PROFIT_STABLE_COIN', 50)
POC_USER = os.environ.get('POC_USER', None)
