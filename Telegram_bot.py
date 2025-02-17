import os

from dotenv import load_dotenv
from telebot import TeleBot

from bag_of_tokens import Bag
from constants import TOKENS_STR, TOKENS_STIKERS
from keyboard import keyboard_add_token, keyboard_main
from exceptions import UnexpectedToken, DontWantAddToken, EmptyBag

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)
bag = Bag()


@bot.message_handler(regexp='Что в мешке?')
def print(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text=f'{bag.__str__()}'
    )


@bot.message_handler(regexp='Добавить жетон')
def add_token(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Какой жетон добавить?',
        reply_markup=keyboard_add_token
    )
    bot.register_next_step_handler(message, add_token_input)


def add_wrong_token(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Какой жетон добавить?',
        reply_markup=keyboard_add_token
    )
    bot.register_next_step_handler(message, add_token_input)


def add_token_input(message):
    chat_id = message.chat.id
    try:
        bag.add_token(message.text)
    except UnexpectedToken:
        bot.send_message(
            chat_id=chat_id,
            text='Такого жетона не существует.\n'
                 'Выберите один из предложеных жетонов.\n'
                 f'Список возможных жетонов:\n{TOKENS_STR}'
        )
        bot.register_next_step_handler(message, add_token_input)
    except DontWantAddToken:
        start(message)
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'Жетон {message.text} добавлен.',
            reply_markup=keyboard_main
        )


@bot.message_handler(regexp='Достать жетон')
def get_token(message):
    chat_id = message.chat.id
    try:
        sticker = TOKENS_STIKERS.get(bag.get_token())
    except EmptyBag:
        bot.send_message(
            chat_id=chat_id,
            text='Мешок пуст',
            reply_markup=keyboard_main
        )
    else:
        bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            reply_markup=keyboard_main
        )


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.reply_to(message, f'айди данного стикера - {message.sticker.file_id}')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text=f'Я мешок, я мешок. Вот что я могу',
        reply_markup=keyboard_main
    )



def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()