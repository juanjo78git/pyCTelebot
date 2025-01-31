# -*- coding: utf-8 -*-

import argparse

from argparse import RawTextHelpFormatter
from pyCTelebot import __version__


def build_parser():
    """ Parser args """
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='pyCTelebot: Your Telegram Bot')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    parser.add_argument('-l', '--lang', metavar='Locale',
                        dest='lang', type=str, default='',
                        help='Select language (es, en)')

    parser.add_argument('-a', '--about',
                        dest='about', action='store_true',
                        help='Show About Us')

    parser.add_argument('-Tp', '--TelegramBotPolling',
                        dest='telebot', action='store_true',
                        help='Select Telegram bot run with polling (without it is Webhook)')

    parser.add_argument('-c', '--cron', type=int,
                        dest='cron', nargs='?', const=5,
                        help='Run cron (default 5 seconds interval)')

    parser.add_argument('-w', '--worker',
                        dest='worker', action='store_true',
                        help='Run worker from cron')

    parser.add_argument('-poc', '--PoC',
                        dest='poc', action='store_true',
                        help='Run Proof of Concept')

    parser.add_argument('-n', '--notices',
                        dest='notice', action='store_true',
                        help='Run notices')

    return parser
