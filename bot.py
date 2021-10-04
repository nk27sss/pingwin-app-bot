import time
import random
import telebot
from telebot import types

import config

active_chats_id=[564291081]

def main():
    bot = telebot.TeleBot(token=config.TOKEN)
    
    # если /help, /start
    @bot.message_handler(commands=['start','stop','id'])
    def send_welcome(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup()
        buttonA = types.KeyboardButton('/start')
        buttonB = types.KeyboardButton('/stop')
        buttonC = types.KeyboardButton('/id')
        markup.row(buttonA, buttonB, buttonC)

        if message.text=="/start":
            bot.send_message(chat_id, f"Здравствуйте. {message.from_user.first_name}! Уведомления программы включены", reply_markup=markup)
            if chat_id not in active_chats_id:
                active_chats_id.append(chat_id)

        if message.text=="/stop":
            bot.send_message(chat_id, f"Здравствуйте. {message.from_user.first_name}! Уведомления программы отключены", reply_markup=markup)
            if chat_id in active_chats_id:
                active_chats_id.remove(chat_id)

        if message.text=="/id":
            if chat_id in active_chats_id:
                s="включены"
            else:
                s="отключены"
            bot.send_message(chat_id, f"ID этого чата: {chat_id} Уведомления программы {s}", reply_markup=markup)
    
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        bot.send_message(message.chat.id, 'It works!')

    def send_status_action_users(text):
        for chat_id in active_chats_id:
            bot.send_message(chat_id, text)


    print("Bot start ")

    send_status_action_users('Бот запущен!')

    # Запускаем постоянный опрос бота в Телеграме
    bot.polling(none_stop=False, interval=0, timeout=200)

    print("END")
if __name__ == '__main__':
    main()