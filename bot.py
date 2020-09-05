
import logging
import os
import os
from pathlib import Path

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PARENT_DIR = Path(__file__).parent
LOG_DIR = os.path.join(PARENT_DIR, 'log')

log_file_path = os.path.join(LOG_DIR, 'bot.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,    
)

TOKEN = os.environ['TOKEN']


PROXY = {
    'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'},
}


def greet_user(update, context):
    print('Called /start')
    update.message.reply_text('Hello, user!')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(
        TOKEN,
        use_context=True,
        request_kwargs=PROXY,
    )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot started!')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
