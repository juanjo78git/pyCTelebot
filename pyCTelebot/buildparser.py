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

    parser.add_argument('-a', '--aboutus',
                        dest='aboutus', action='store_true', 
                        help='Show About Us')
                        
    return parser
