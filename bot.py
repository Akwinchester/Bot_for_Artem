import os.path
import shutil

import telebot
from telebot import types
from settings import tn
from my_functions import add_row_for_csv_file, past_link
from shutil import make_archive
from google_sheets import GoogleSheet

bot = telebot.TeleBot(tn)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Текст')
    item_2 = types.KeyboardButton('Фото')
    item_3 = types.KeyboardButton('Аудио')
    item_4 = types.KeyboardButton('Видео')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)

    bot.send_message(message.chat.id, 'Привет, здесь ты можешь загрузить файлы', reply_markup=markup)


@bot.message_handler(content_types=['text', 'photo', 'document', 'audio', 'video'])
def body(message):
    user_name = message.from_user.first_name
    gs = GoogleSheet()
    if message.text == 'Текст':
        bot.send_message(message.chat.id, 'Отправте текстовый документ')
    elif message.text == 'Фото':
        bot.send_message(message.chat.id, 'Отправьте фото')
    elif message.text == 'Видео':
        bot.send_message(message.chat.id, 'Отправьте видео')
    elif message.text == 'Аудио':
        bot.send_message(message.chat.id, 'Отправьте аудиофайл')

    if message.photo:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/{file_info.file_path}', 'wb') as f:
                f.write(downloaded_file)

            file_name = file_info.file_path.split('/')[-1]
            add_row_for_csv_file(user_name, message.content_type, file_name, f'./{file_info.file_path}')
            gs.add('Лист1!A1', values=[user_name, past_link(file_name, f'./{file_info.file_path}')])
            bot.send_message(message.chat.id, 'фото загружено')
        except Exception as e:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')

    elif message.document:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/documents/{message.document.file_name}', 'wb') as f:
                f.write(downloaded_file)

            add_row_for_csv_file(user_name, message.content_type, message.document.file_name, f'./documents/{message.document.file_name}')
            bot.send_message(message.chat.id, 'документ загружен')
        except Exception as e:
            print(e)
            print('ошибка загрузки документа')
            bot.send_message(message.chat.id, 'ошибка загрузки документа')

    elif message.audio:
        try:
            file_info = bot.get_file(message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/{file_info.file_path}', 'wb') as f:
                f.write(downloaded_file)

            file_name = file_info.file_path.split('/')[-1]
            add_row_for_csv_file(user_name, message.content_type, file_name, f'./{file_info.file_path}')
            bot.send_message(message.chat.id, 'аудиофайл загружен')
        except:
            print('ошибка загрузки аудио')
            bot.send_message(message.chat.id, 'ошибка загрузки аудио')

    elif message.video:
        try:
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/{file_info.file_path}', 'wb') as f:
                f.write(downloaded_file)

            file_name = file_info.file_path.split('/')[-1]
            add_row_for_csv_file(user_name, message.content_type, file_name, f'./{file_info.file_path}')
            bot.send_message(message.chat.id, 'видео загружено')
        except:
            print('ошибка загрузки видео')
            bot.send_message(message.chat.id, 'ошибка загрузки видео')

    shutil.make_archive('files_archive', 'zip', './files')


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)