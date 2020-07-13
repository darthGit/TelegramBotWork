#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
"""
Basic example for a bot that uses inline keyboards.
"""

import sys
from commands import common
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler, Filters)
from config import *
sys.path.append('..')


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(Config.TOKEN, use_context=True)

    covn_handler = ConversationHandler(
        entry_points=[CommandHandler('start', common.start)],

        states={
            Config.CHOOSING: [MessageHandler(Filters.regex('^(Search)$'), common.regular_choice, pass_user_data=True),
                              MessageHandler(Filters.regex('^(Ping)$'), common.start_ping)],

            Config.SEARCH: [MessageHandler(Filters.text, common.search)],

            Config.CHOOSEHOST: [MessageHandler(Filters.text, common.run_command)],

            Config.STARTPING : [MessageHandler(Filters.text, common.command_ping)],

            Config.ACTIONFORSHOP : [MessageHandler(Filters.regex('^(Ping router)$'), None),
                                    MessageHandler(Filters.regex('^(Ping server and AMT)$'), None),
                                    MessageHandler(Filters.regex('^(Ping switch)$'), None),
                                    MessageHandler(Filters
                                                   .regex('^(Ping other host in shop)$'), None),
                                    MessageHandler(Filters
                                                   .regex('^(Actions for kassa)$'), common.choose_host),
                                    CallbackQueryHandler(common.button, pass_update_queue=False)],
            Config.ACTIONFORHOST : [MessageHandler(Filters.regex('^(Reboot)$'), None),
                                    MessageHandler(Filters.regex('^(Delete check)$'), None),
                                    MessageHandler(Filters.regex('^(killall)$'), None),
                                    MessageHandler(Filters.regex('^(Ping this host)$'), None),
                                    MessageHandler(Filters.regex('^(Get screenshot)$'), None),
                                    MessageHandler(Filters.regex('^(Get TTY)$'), None),
                                    MessageHandler(Filters.regex('^(Set TTY)$'), None),
                                    MessageHandler(Filters
                                                   .regex('^(Get TTY and devices in custom.cfg)$')
                                                   , None),
                                    MessageHandler(Filters.regex('^(EXIT)$'), None)]

        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), common.start)]
    )

    updater.dispatcher.add_handler(covn_handler)
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(common.error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
