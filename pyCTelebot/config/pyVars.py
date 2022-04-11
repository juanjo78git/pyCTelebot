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

# Cron Interval in seconds
CRON_INTERVAL = int(os.environ.get('CRON_INTERVAL', 5))
