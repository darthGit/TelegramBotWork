

import logging, subprocess, shlex

import config
import exec_comands

from telegram.ext import Updater, CommandHandler

TOKEN = config.Config.TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi, Use /ping <ip> to ping')

def set_job(update, context):
    logger.info
    try:
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        context.user_data['chat_id'] = update.message.chat_id
        context.user_data['ip_adr'] = str(context.args[0])
        new_job = context.job_queue.run_once(ping, 1, context=context)
        context.chat_data['job'] = new_job
        update.message.reply_text('Ping successfully run!')

    except (IndexError, ValueError):
        update.message.reply_text('Hi, Use /ping <ip> to ping')



def ping(context):
    job = context.job 
    #ps = subprocess.Popen(['ping', job.context.user_data['ip_adr'], '-c 5'], stdout=subprocess.PIPE)
    #out = ps.communicate()[0]
    #print(out)
    #out = run_command('ping ' + job.context.user_data['ip_adr'] + ' -c 5')
    #context.bot.send_message(job.context.user_data['chat_id'], text=str(out))
    res = exec_comands.ExeComands().run_ping(ip_adress=job.context.user_data['ip_adr'])

    context.bot.send_message(job.context.user_data['chat_id'], text=res)


def job_ping(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        ip_adr = str(context.args[0])
        if ip_adr == "":
            update.message.reply_text('Sorry, use /ping <ip> !')
            return

        # Add job to queue and stop current one if there is a timer already
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        context.user_data['ip_adr'] = ip_adr
        context.user_data['chat_id'] = chat_id
        new_job = context.job_queue.run_once(ping, 0, context=context)
        context.chat_data['job'] = new_job

        update.message.reply_text('Ping successfully run!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /ping <ip>')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("ping", job_ping,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    logger.info('Starting polling....')
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()