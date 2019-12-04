"""
Simple Lvivcold Telegram bot



author = Burko Bogdan
"""

TOKEN = '966337942:AAE0FiNCyhcR-nNMdGBn1bBqg0rGCw72t48'

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


REGISTR, REGADMIN = range(2)

def start(update, context):
    update.message.reply_text('Реєстрація в системі ')

    return REGISTR



def registration(update, context):
    reply_keyboard = [['user', 'admin']]

    update.message.reply_text('Хто ви?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return REGADMIN


def regAdmin(update, context):
    logger.info("log: regAdmin() %s", update.message.text)
    update.message.reply_text('Для реєстрації адміністратора введіть вашу електрону пошту на Львівхолоді')


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    """Run bot"""
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTR: [MessageHandler(Filters.text, registration)],

            REGADMIN: [MessageHandler(Filters.regex('^(user|admin)$'), regAdmin)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
#    dispatcher.add_handler(CommandHandler("start", start))
 #   dispatcher.add_handler(CommandHandler("registration", registration))
  #  dispatcher.add_handler(CommandHandler("admin", regAdmin))

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
