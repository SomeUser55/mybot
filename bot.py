
import logging

import settings


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    filename=settings.log_file_path,
    level=logging.INFO,    
)


def greet_user(update, context):
    print('Called /start')
    update.message.reply_text('Hello, user!')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(
        settings.TOKEN,
        use_context=True,
        request_kwargs=settings.PROXY,
    )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot started!')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
