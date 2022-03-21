# -*- coding: utf-8 -*-

from pyCTelebot import buildparser
import os
import sys
import gettext
import json
import logging
from pyCTelebot import pyTelegram

_ = gettext.gettext


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

    clearscr()
    print('Locale: ' + os.environ['LANG'])

    if options.aboutus:
        print(printaboutus())
        exit()

    if options.telebot:
        pyTelegram.run(how='p')
    else:
        pyTelegram.run(how='w')

    # TODO: Do something
    # pyTelegram.run()
    exit()


# Clear screen function
def clearscr():
    osname = os.name
    if osname == 'posix':
        os.system('clear')
    elif osname == 'nt' or osname == 'dos':
        os.system('cls')
    else:
        print('\n' * 30)


def printaboutus():
    # TODO: poedit to generate .pot, .po and .mo
    txt = _('text_aboutus')
    return txt


if __name__ == '__main__':
    main()

