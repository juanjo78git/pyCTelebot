# -*- coding: utf-8 -*-

from pyCTelebot.utils import pyBuildParser, pyTelegram, pyNotices
import os
import sys
import gettext
import logging
from pyCTelebot import pyCryptoCron, pyCryptoWorker
from pyCTelebot.config.pyVars import ENV_CONFIG
from pyCTelebot import pyPoC

# i18n
_ = gettext.gettext
# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[
                        logging.StreamHandler(sys.stdout)
                    ]
                    )
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


def main():
    # Get Args
    parser = pyBuildParser.build_parser()
    options = parser.parse_args()
    # gettext
    if options.lang != '':
        os.environ['LANG'] = options.lang
    else:
        if sys.platform.startswith('win'):
            import locale
            if os.getenv('LANG') is None:
                lang, _env = locale.getdefaultlocale()
                os.environ['LANG'] = lang
    gettext.textdomain('pyCTelebot')
    gettext.bindtextdomain('pyCTelebot', './pyCTelebot/locale')

    clear_screen()
    logger.log(msg='Locale: {0}'.format(os.environ['LANG']), level=logging.DEBUG)

    if options.poc:
        logger.log(msg='PoC start', level=logging.INFO)
        pyPoC.run()
        logger.log(msg='PoC ends', level=logging.INFO)
        exit()

    if options.about:
        print(print_about_us())
        exit()

    if options.worker:
        pyCryptoWorker.run()
        logger.log(msg='Worker ends', level=logging.INFO)
        exit()

    if options.cron:
        print(options.cron)
        pyCryptoCron.run(seconds=options.cron)
        logger.log(msg='Cron ends', level=logging.INFO)
        exit()

    if options.notice:
        pyNotices.run()
        logger.log(msg='Notice ends', level=logging.INFO)
        exit()

    if options.telebot:
        pyTelegram.run(how='p')
    else:
        pyTelegram.run(how='w')

    exit()


# Clear screen function
def clear_screen():
    osname = os.name
    if osname == 'posix':
        os.system('clear')
    elif osname == 'nt' or osname == 'dos':
        os.system('cls')
    else:
        print('\n' * 30)


def print_about_us():
    # TODO: poedit to generate .pot, .po and .mo
    txt = _('text_about')
    return txt


if __name__ == '__main__':
    main()
