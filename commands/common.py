from utility import findIp, exec_comands
from log.logging import logger
from config import *

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def start(update, context):
    logger.info('call')
    update.message.reply_text('Please choose :', reply_markup=get_search_keyboard())
    return Config.CHOOSING

def ping(update, context):
    logger.info('function ping')
    user_data = context.user_data
    for key, value in user_data.items():
        logger.info('[{}] - [{}]'.format(key, value))
    ipaddr = '192.168.' + value + '.2'
    exec_comands.ExeComands().run_killall(ip_adress=ipaddr)
    update.message.reply_text('Please choose :', reply_markup=get_search_keyboard())
    return Config.CHOOSING


def regular_choice(update, context):
    logger.info('call')
    text = update.message.text
    logger.info(text)
    update.message.reply_text("Please enter shop name!")

    return Config.SEARCH

def start_ping(update, context):
    logger.info('call')
    update.message.reply_text('Please enter ip adress:')
    return Config.STARTPING

def command_ping(update, context):
    user_data = context.user_data
    print(user_data.items())
    print('commad_ping()')
    text = update.message.text
    update.message.reply_text("Please wait, ping was started!")
    result = exec_comands.ExeComands().run_ping(ip_adress=text)
    print(result)
    update.message.reply_text(result)
    update.message.reply_text('Please choose (Start function):', reply_markup=get_search_keyboard())
    return Config.CHOOSING


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
        return Config.ACTIONFORSHOP
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
    return Config.ACTIONFORSHOP

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def get_search_keyboard():
    reply_keyboard = [['Search','Ping']]
    reply_keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return reply_keyboard_markup