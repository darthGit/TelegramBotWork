#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import sys
sys.path.append('..')
import config
from utility import findIp
from utility import exec_comands


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                            ConversationHandler,
                            MessageHandler, Filters)

TOKEN = config.Config.TOKEN
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s()',
                    level=logging.INFO)
logger = logging.getLogger('utility.testCode2')

CHOOSING, SEARCH, STARTPING, ACTIONFORHOST, ACTIONFORSHOP = range(5)

reply_keyboard = [['Search','Ping']]

reply_keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) 

def ping(update, context):
    logger.info('function ping')
    user_data = context.user_data
    for key, value in user_data.items():
        logger.info('[{}] - [{}]'.format(key, value))
    update.message.reply_text('Please choose :', reply_markup=reply_keyboard_markup)
    return CHOOSING

def start(update, context):
    logger.info('call')
    update.message.reply_text('Please choose :', reply_markup=reply_keyboard_markup)
    return CHOOSING

def regular_choice(update, context):
    logger.info('call')
    text = update.message.text
    logger.info(text)
    update.message.reply_text("Please enter shop name!")

    return SEARCH

def start_ping(update, context):
    logger.info('call')
    update.message.reply_text('Please enter ip adress:')
    return STARTPING

def command_ping(update, context):
    user_data = context.user_data
    print(user_data.items())
    print('commad_ping()')
    text = update.message.text
    update.message.reply_text("Please wait, ping was started!")
    result = exec_comands.ExeComands().run_ping(ip_adress=text)
    print(result)
    update.message.reply_text(result)
    update.message.reply_text('Please choose (Start function):', reply_markup=reply_keyboard_markup)
    return CHOOSING

def search(update, context):
    chat_id = update.message.chat_id
    shop_name = update.message.text
    keyboard = []
    try:
        #shop_name = str(context.args[0])
        if shop_name == "":
            update.message.reply_text('Sorry, use /search <name of shop> !')
            return
        for shop_item in findIp.find_shop(shop_name):
            keyboard.append(InlineKeyboardButton(shop_item[1], callback_data=shop_item[0]))

        reply_markup = InlineKeyboardMarkup.from_column(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)
        return ACTIONFORSHOP
    except (IndexError, ValueError):
        update.message.reply_text('Sorry, use /search <name of shop> !')

def button(update, context):
    query = update.callback_query
    context.user_data['ip_addres'] = "{}".format(query.data)
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))

    host_action_keyboard = [['Ping router','Ping server and AMT', 'Ping switch', 'Ping other host in shop', 'Actions for kassa']]

    host_action_keyboard_markup = ReplyKeyboardMarkup(host_action_keyboard, one_time_keyboard=True) 

    query.message.reply_text('Please choose (Start function):', reply_markup=host_action_keyboard_markup)
    return ACTIONFORSHOP


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    covn_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Search)$'), regular_choice),
                        MessageHandler(Filters.regex('^(Ping)$'), start_ping)],

            SEARCH: [MessageHandler(Filters.text, search)],

            STARTPING : [MessageHandler(Filters.text, command_ping)],

            ACTIONFORSHOP : [MessageHandler(Filters.regex('^(Ping router)$'), None),
                                MessageHandler(Filters.regex('^(Ping server and AMT)$'), None),
                                MessageHandler(Filters.regex('^(Ping switch)$'), None),
                                MessageHandler(Filters.regex('^(Ping other host in shop)$'), None),
                                MessageHandler(Filters.regex('^(Actions for kassa)$'), ping),
                                CallbackQueryHandler(button, pass_update_queue=False)
                            ],
            ACTIONFORHOST : [MessageHandler(Filters.regex('^(Reboot)$'), None),
                                MessageHandler(Filters.regex('^(Delete check)$'), None),
                                MessageHandler(Filters.regex('^(killall)$'), None),
                                MessageHandler(Filters.regex('^(Ping this host)$'), None),
                                MessageHandler(Filters.regex('^(Get screenshot)$'), None),
                                MessageHandler(Filters.regex('^(Get TTY)$'), None),
                                MessageHandler(Filters.regex('^(Set TTY)$'), None),
                                MessageHandler(Filters.regex('^(Get TTY and devices in custom.cfg)$'), None),
                                MessageHandler(Filters.regex('^(EXIT)$'), None)
                            ]

        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), start)]
    )

    #updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(covn_handler)
    #updater.dispatcher.add_handler(CallbackQueryHandler(button, pass_update_queue=True))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    #updater.dispatcher.add_handler(CommandHandler('search', search))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()