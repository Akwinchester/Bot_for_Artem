import os.path
import shutil

import telebot
from telebot import types
from settings import tn, ADMIN_ID
from my_functions import add_row_for_csv_file, past_link
from shutil import make_archive
from google_sheets import GoogleSheet
import requests
from test import upload_to_folder


bot = telebot.TeleBot(tn)
user_last_command = {}
def writing_file_to_server(message, type_dir, file_name=None):
    if type_dir == 'video_view_bottom':
        try:
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.split('/')[-1]
            with open(f'./files/video_view_bottom/{file_name}', 'wb') as f:
                f.write(downloaded_file)
            bot.send_message(message.chat.id, 'видео загружено')
        except:
            print('ошибка загрузки видео')
            bot.send_message(message.chat.id, 'ошибка загрузки видео')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir == 'photo_view_from_office_window':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.split('/')[-1]
            with open(f'./files/photo_view_from_office_window/{file_name}', 'wb') as f:
                f.write(downloaded_file)
            bot.send_message(message.chat.id, 'фото загружено')
        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir== 'photo_in_the_opening_year':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.split('/')[-1]
            with open(f'./files/photo_in_the_opening_year/{file_name}', 'wb') as f:
                f.write(downloaded_file)
            bot.send_message(message.chat.id, 'фото загружено')
        except Exception as e:
            print('ошибка загрузки фото', e)
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir == 'drawings_bank_future':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.split('/')[-1]
            with open(f'./files/drawings_bank_future/{file_name}', 'wb') as f:
                f.write(downloaded_file)
            bot.send_message(message.chat.id, 'фото загружено')
        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)



@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Фотографии в год открытия')
    item_2 = types.KeyboardButton('Рисунки "Банк будущего"')
    item_3 = types.KeyboardButton('Видео "Взгляд снизу"')
    item_4 = types.KeyboardButton('Фотография с видом из окна офиса')
    item_5 = types.KeyboardButton('5-кнопка')
    item_6 = types.KeyboardButton('Задать вопрос')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5, item_6)

    bot.send_message(message.chat.id, 'Привет, здесь ты можешь загрузить файлы', reply_markup=markup)




@bot.message_handler(content_types=['text'])
def body(message):
    user_name = message.from_user.first_name
    gs = GoogleSheet()

    if message.text == 'Фотографии в год открытия':
        bot.send_message(message.chat.id, 'Отправьте фото')
        user_last_command[message.chat.id] = 'photo_in_the_opening_year'

    elif message.text == 'Рисунки "Банк будущего"':
        bot.send_message(message.chat.id, 'Отправьте фото')
        user_last_command[message.chat.id] = 'drawings_bank_future'

    elif message.text == 'Видео "Взгляд снизу"':
        bot.send_message(message.chat.id, 'Отправьте видео')
        user_last_command[message.chat.id] = 'video_view_bottom'

    elif message.text == 'Фотография с видом из окна офиса':
        bot.send_message(message.chat.id, 'Отправьте фото')
        user_last_command[message.chat.id] = 'photo_view_from_office_window'




@bot.message_handler(content_types=['photo', 'video'])
def body(message):
    writing_file_to_server(message, user_last_command[message.chat.id])
    del user_last_command[message.chat.id]

if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)