import os.path
import shutil

import telebot
from telebot import types
from settings import tn, ADMIN_ID, id_dir_on_drive
from my_functions import add_row_for_csv_file, past_link
from shutil import make_archive
import requests
import json
from google_service import upload_to_folder, add


bot = telebot.TeleBot(tn)
user_last_command = {}
register_users = {}

if os.path.exists('./users.json'):
    with open('./users.json', 'r', encoding="utf-8") as f:
        register_users = json.load(f)


def writing_file_to_server(message, type_dir, file_name=None):
    if type_dir == 'video_view_bottom':
        bot.send_message(message.chat.id, message)
        try:
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.split('/')[-1]
            with open(f'./files/video_view_bottom/{file_name}', 'wb') as f:
                f.write(downloaded_file)
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
            bot.send_message(message.chat.id, 'Спасибо ! Еще немного и ты увидишь насколько ярче и интересней станет ValuesFest 2022 благодаря тебе! Проверь остальные категории, может, есть еще что-то интересное, чем ты еще не поделился?)')
        except ApiTelegramException:
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
            bot.send_message(message.chat.id, 'Спасибо ! Еще немного и ты увидишь насколько ярче и интересней станет ValuesFest 2022 благодаря тебе! Проверь остальные категории, может, есть еще что-то интересное, чем ты еще не поделился?)')
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
            bot.send_message(message.chat.id, 'Спасибо ! Еще немного и ты увидишь насколько ярче и интересней станет ValuesFest 2022 благодаря тебе! Проверь остальные категории, может, есть еще что-то интересное, чем ты еще не поделился?)')
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
            bot.send_message(message.chat.id, 'Спасибо ! Еще немного и ты увидишь насколько ярче и интересней станет ValuesFest 2022 благодаря тебе! Проверь остальные категории, может, есть еще что-то интересное, чем ты еще не поделился?)')
        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir == 'photo_before_after':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.split('/')[-1]
            with open(f'./files/photo_before_after/{file_name}', 'wb') as f:
                f.write(downloaded_file)
            bot.send_message(message.chat.id, 'Спасибо ! Еще немного и ты увидишь насколько ярче и интересней станет ValuesFest 2022 благодаря тебе! Проверь остальные категории, может, есть еще что-то интересное, чем ты еще не поделился?)')
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
    item_5 = types.KeyboardButton('Фотографии "До/после"')
    item_6 = types.KeyboardButton('Задать вопрос')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5, item_6)

    bot.send_message(message.chat.id, '''Привет! 
Спасибо, что решил поучаствовать в создании Values Fest 2022! 
Пожалуйста, представься, чтобы мы знали всех наших героев по именам)'''
, reply_markup=markup)

    bot.send_message(message.chat.id, f'''Отправь мне такое сообщение
ригистрация:ФИО''')




@bot.message_handler(content_types=['text'])
def body(message):
    global register_users
    register_message_command = None
    register_name = None
    if ':' in message.text:
        register_message_command = str(message.text).split(':')[0]
        register_name = str(message.text).split(':')[1]
    user_name = message.from_user.first_name

    if register_message_command == 'Регистрация' or register_message_command == 'регистрация':
        register_users[str(message.chat.id)] = register_name
        with open('./users.json', 'w',encoding="utf-8") as f:
            json.dump(register_users, f, ensure_ascii=False)
        if os.path.exists('./users.json'):
            with open('./users.json', 'r', encoding="utf-8") as f:
                register_users = json.load(f)

        bot.send_message(message.chat.id, '''Очень рады познакомиться!
Выбирай контент, которым тебе хочется поделиться, чтобы его увидели все участники фестиваля! 
''')

    if message.text == 'Фотографии в год открытия':
        bot.send_message(message.chat.id, '''1996 год. В России открывается первое отделение Райффайзен Банк, а чем ты занимаешься в 1996? Ты уже работаешь и развиваешь свои профессиональные навыки? Или ты учишься в Университете и готовишься к защите диплома? Может, ты еще в школе, выбираешь свое будущее и мечтаешь стать космонавтом? Или ты тот самый милый малыш у новогодней елки в детском саду? Найди свое фото из 1996 года, отсканируй или сфотографируй на телефон и пришли его, пожалуйста, нам) 
И не забудь написать свое имя, мы должны знать своих героев)''')
        user_last_command[message.chat.id] = 'photo_in_the_opening_year'


    elif message.text == 'Рисунки "Банк будущего"':
        bot.send_message(message.chat.id, '''Спорим, Ваш ребенок - очень талантливый художник с безграничной фантазией? Докажите это всем! Вот Вам и Вашему юному таланту небольшое домашнее задание - нарисовать рисунок на тему “Банк будущего”. Никаких ограничений по техникам, масштабам и форматам)''')
        user_last_command[message.chat.id] = 'drawings_bank_future'

    elif message.text == 'Видео "Взгляд снизу"':
        bot.send_message(message.chat.id, '''У вас есть дети? Они точно знают где Вы работаете? Давайте снимем с ними небольшое интервью в стиле “Взгляд снизу” 
Технические характеристики для видео: *заполнить исполнителем видеоконтента*''')
        user_last_command[message.chat.id] = 'video_view_bottom'


    elif message.text == 'Фотография с видом из окна офиса':
        bot.send_message(message.chat.id, 'За 26 лет география наших офисов разрослась по всей России! Пришлите фото с видом из окна Вашего офиса с указанием города, у нас будет захватывающая игра, в которой будет и Ваше фото)')
        user_last_command[message.chat.id] = 'photo_view_from_office_window'
    elif message.text == 'Фотографии "До/после"':
        bot.send_message(message.chat.id, 'Признайтесь, вам нравится смотреть подборки «Было/Стало» или «До/После») Покажите и вы нам, какой путь вы прошли и как изменились за 26 лет! Пришлите нам две свои фотографии: из 1996 и 2022 года, а мы превратим это в интерактивную фотогалерею на Values Fest 2022!')
        user_last_command[message.chat.id] = 'photo_before_after'
    elif message.text == 'Задать вопрос':
        bot.send_message(message.chat.id, 'Опишите проблему')
        user_last_command[message.chat.id] = 'question'

    elif message.chat.id in user_last_command:
        if user_last_command[message.chat.id] == 'question':
            bot.send_message(ADMIN_ID, f'{message.from_user.first_name} {message.from_user.last_name}')
            bot.send_message(ADMIN_ID, message.text)



@bot.message_handler(content_types=['photo', 'video'])
def body(message):
    if str(message.chat.id) in register_users:
        user_name = register_users[str(message.chat.id)]
    else:
        print('проблемы с регистрацией')
        user_name = f'{message.from_user.last_name} {message.from_user.first_name}'
    if message.photo:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    elif message.video:
        file_info = bot.get_file(message.video.file_id)
    file_name = file_info.file_path.split('/')[-1]
    writing_file_to_server(message, user_last_command[message.chat.id])

    upload_to_folder(real_folder_id=id_dir_on_drive[user_last_command[message.chat.id]], file_for_load=f'./files/{user_last_command[message.chat.id]}/{file_name}', file_name=file_name, user_name=user_name)

    add_row_for_csv_file(user_name=user_name, dir=user_last_command[message.chat.id], name_file=file_name, link_for_file=f'./{user_last_command[message.chat.id]}/{file_name}')
    shutil.make_archive('files_archive', 'zip', './files')
    del user_last_command[message.chat.id]

if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)