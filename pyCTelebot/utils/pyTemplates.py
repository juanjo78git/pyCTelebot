# -*- coding: utf-8 -*-
import json
import gettext
import logging
from pyCTelebot.config.pyVars import ENV_CONFIG

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


def templates_json(values: json = None, template_type: str = None):
    if values is None:
        return values
    if template_type == 'all_balances':
        return json.dumps(values, indent=4, sort_keys=True)
    else:
        return json.dumps(values, indent=4, sort_keys=True)
