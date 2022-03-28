# -*- coding: utf-8 -*-

from pyCTelebot import buildparser
import os
import sys
import gettext
import json
import logging
from pyCTelebot import pyTelegram, pyCryptoCron, pyCryptoWorker

# i18n
_ = gettext.gettext
# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    # Get Args
    parser = buildparser.build_parser()
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
    logger.log(msg='Locale: {0}'.format(os.environ['LANG']), level=logging.INFO)

    if options.aboutus:
        print(print_about_us())
        exit()

    if options.worker:
        pyCryptoWorker.run()
        exit()

    if options.cron:
        pyCryptoCron.run()
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
    txt = _('text_aboutus')
    return txt


if __name__ == '__main__':
    main()

