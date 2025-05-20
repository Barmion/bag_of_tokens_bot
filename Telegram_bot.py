import os

from dotenv import load_dotenv
from telebot import TeleBot

import bag_of_tokens
from constants import TOKENS_STR, TOKENS_STIKERS
from keyboard import keyboard_add_token, keyboard_main
from exceptions import (
    UnexpectedToken,
    DontWantAddToken,
    EmptyBag,
    DontWantDeleteToken
)
import db
import keyboard

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(regexp='Что в мешке?')
def print(message):
    chat_id = message.chat.id
    text = bag_of_tokens.what_in_bag(id=chat_id)
    bot.send_message(
        chat_id=chat_id,
        text=text
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


def add_token_input(message):
    chat_id = message.chat.id
    try:
        bag_of_tokens.add_token(token=message.text, table='bags', id=chat_id)
    except UnexpectedToken:
        bot.send_message(
            chat_id=chat_id,
            text='Такого жетона не существует.\n'
                 'Выберите один из предложеных жетонов.\n'
                 f'Список возможных жетонов:\n{TOKENS_STR}'
        )
        bot.register_next_step_handler(message, add_token_input)
    except DontWantAddToken:
        start_message(message)
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'Жетон {message.text} добавлен.',
            reply_markup=keyboard_main
        )


@bot.message_handler(regexp='Удалить жетон')
def delete_token(message):
    chat_id = message.chat.id
    if bag_of_tokens.what_in_bag(id=chat_id) != 'Мешок пуст':
        bot.send_message(
            chat_id=chat_id,
            text='Какой жетон удалить?',
            reply_markup=keyboard.keyboard_delete_token(chat_id)
        )
        bot.register_next_step_handler(message, delete_token_input)
    else:
        bot.send_message(
            chat_id=chat_id,
            text='Мешок пуст',
            reply_markup=keyboard_main
        )


def delete_token_input(message):
    chat_id = message.chat.id
    try:
        bag_of_tokens.delete_token(
            token=message.text,
            table='bags',
            id=chat_id
        )
    except UnexpectedToken:
        bot.send_message(
            chat_id=chat_id,
            text='Такого жетона не существует.\n'
                 'Выберите один из предложеных жетонов.\n'
                 f'Список возможных жетонов:\n{TOKENS_STR}'
        )
        bot.register_next_step_handler(message, delete_token_input)
    except DontWantDeleteToken:
        start_message(message)
    except EmptyBag:
        bot.send_message(
            chat_id=chat_id,
            text='Мешок пуст',
            reply_markup=keyboard_main
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'Жетон {message.text} удалён.',
            reply_markup=keyboard_main
        )


@bot.message_handler(regexp='Достать жетон')
def get_token(message):
    chat_id = message.chat.id
    try:
        token = bag_of_tokens.get_token(id=chat_id)
        sticker = TOKENS_STIKERS.get(token)
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
        db.add_token(token=token, table='users_stats', id=chat_id)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    db.new_user(id=chat_id)
    start_message(message)


@bot.message_handler(commands=['home'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Я мешок, я мешок. Вот что я могу',
        reply_markup=keyboard_main
    )


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
