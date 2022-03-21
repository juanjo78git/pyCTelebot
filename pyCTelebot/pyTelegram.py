# -*- coding: utf-8 -*-


from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from pyCTelebot.config.auth import TOKEN_TELEGRAM, WEBHOOK_URL_TELEGRAM, PORT
from pyCTelebot import pyCrypto

import gettext
_ = gettext.gettext

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def run(how):

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

    pricecoin_handler = CommandHandler('pricecoin', priceCoin)
    dispatcher.add_handler(pricecoin_handler)

    # Ultimo evento para comandos desconocidos.
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Controlador de errores
    # dispatcher.add_error_handler(error_callback)

    # Comienza el bot
    print('Hello Bot!')

    if how == 'w':
        # O se arranca con webhook
        logger.log(msg='Start with webhook', level=logging.INFO)
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN_TELEGRAM, webhook_url=WEBHOOK_URL_TELEGRAM + TOKEN_TELEGRAM)
    else:
        # O se arranca con polling
        logger.log(msg='Start with polling', level=logging.INFO)
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


def priceCoin(update: Update, context: CallbackContext):
    if len(update.effective_message.text.split(None, 1)) == 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=_("Coin: {0} Price: {1}").format(
            update.effective_message.text.split(None, 1)[1], pyCrypto.price(coin=update.effective_message.text.split(None, 1)[1])
        ))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=_("Error params"))


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=_("Sorry, I didn't understand that command."))

