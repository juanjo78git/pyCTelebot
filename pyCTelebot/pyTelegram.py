# -*- coding: utf-8 -*-


from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from config.auth import TOKEN_TELEGRAM


import gettext
_ = gettext.gettext

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def run():

    # Conexion
    updater = Updater(token=TOKEN_TELEGRAM, use_context=True)
    dispatcher = updater.dispatcher

    # Eventos que activarán nuestro bot.
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # Ultimo evento para comandos desconocidos.
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Controlador de errores
    # dispatcher.add_error_handler(error_callback)
    # Comienza el bot
    print('Hello Bot!')
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()


# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=_("I'm a great bot!!"))


def stop(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=_("Bye!!"))


# Eco de lo que digas
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=(" {0} " + _("said:") + " {1}").format(
        update.effective_user.first_name, update.message.text))


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=_("Sorry, I didn't understand that command."))

