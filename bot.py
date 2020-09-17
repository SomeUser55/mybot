
import logging
from random import randint, choice
from glob import glob
import traceback

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize

import settings


logging.basicConfig(
    filename=settings.log_file_path,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s| %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logging.getLogger().addHandler(logging.StreamHandler())


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)

    return user_data['emoji']


def greet_user(update, context):
    print('Called /start')
    print(update)
    print(context)
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    update.message.reply_text(
        f"Hello, {username} {context.user_data['emoji']}!",
    )


def talk_to_me(update, context):
    print('Called talk')
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(
        f"You write: {user_text}\n{context.user_data['emoji']}",
    )


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        res = 'You win'
    elif user_number == bot_number:
        res = 'Tie game'
    else:
        res = 'I won'

    return f"Your number {user_number}. My number {bot_number}. {res}!"


def guess_number(update, context):
    print('Called guess')
    print(update)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            traceback.print_exc()
            logging.error(traceback.format_exc())
            message = 'Not a number!'
    else:
        message = 'Enter integer number'

    print(message)
    update.message.reply_text(message)


def send_cat_picture(update, context):
    print('Called cat')
    cat_photos_list = glob(settings.IMAGE_PATTERN)
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_pic_filename, 'rb'),
    )


def main():
    mybot = Updater(
        settings.TOKEN,
        use_context=True,
        request_kwargs=settings.PROXY,
    )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot started!')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
