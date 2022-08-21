import os.path
import shutil

import telebot
from telebot import types
from settings import tn, ADMIN_ID, id_dir_on_drive, MODERATOR_CHAT_LINK
from my_functions import add_row_for_csv_file, past_link
from shutil import make_archive
import requests
import json
from google_service import upload_to_folder, add


bot = telebot.TeleBot(tn)
user_last_command = {}
group_photo = {}
register_users = {}
city_user = {}
flag_city_user = []


if os.path.exists('./users.json'):
    with open('./users.json', 'r', encoding="utf-8") as f:
        register_users = json.load(f)


def writing_file_to_server(message, type_dir, count, file_name, file_info, user_name, phone_number):
    if type_dir == 'video_view_bottom':
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/video_view_bottom/{file_name}', 'wb') as f:
                f.write(downloaded_file)
        except:
            print('ошибка загрузки видео')
            bot.send_message(message.chat.id, 'ошибка загрузки видео')
            bot.send_message(ADMIN_ID,
                             f'пользователь: {user_name} отправил видео. Телефон: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    elif type_dir == 'photo_view_from_office_window':
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_view_from_office_window/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.send_message(ADMIN_ID,
                             f'пользователь: {user_name} отправил фото {type_dir}. Телефон: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    elif type_dir== 'photo_in_the_opening_year':
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_in_the_opening_year/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except Exception as e:
            print('ошибка загрузки фото', e)
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.send_message(ADMIN_ID,
                             f'пользователь: {user_name} отправил фото {type_dir}. Телефон: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    elif type_dir == 'drawings_bank_future':
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/drawings_bank_future/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.send_message(ADMIN_ID,
                             f'пользователь: {user_name} отправил фото {type_dir}. Телефон: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    elif type_dir == 'photo_before_after':
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_before_after/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.send_message(ADMIN_ID,
                             f'пользователь: {user_name} отправил фото {type_dir}. Телефон: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    if count == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_1 = types.KeyboardButton('Фотографии в год открытия')
        item_2 = types.KeyboardButton('Рисунки "Банк будущего"')
        item_3 = types.KeyboardButton('Видео "Взгляд снизу"')
        item_4 = types.KeyboardButton('Фотография с видом из окна офиса')
        item_5 = types.KeyboardButton('Фотографии "До/после"')
        item_6 = types.KeyboardButton('Задать вопрос')
        item_7 = types.KeyboardButton('Контент загружен')
        markup.add(item_1, item_2)
        markup.add(item_3, item_4)
        markup.add(item_5)
        markup.add(item_6, item_7)
        bot.send_message(message.chat.id, 'Спасибо, что поделились с нами своей историей ! Если вы проверили все категории и закончили, пожалуйста, нажмите кнопку “Контент загружен”', reply_markup=markup)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    item_inline_1 = types.InlineKeyboardButton('Регистрация', callback_data='register')
    markup_inline.add(item_inline_1)
    bot.send_message(message.chat.id, 'Привет! Спасибо, что решили поучаствовать в создании Values Fest 2022! Пожалуйста, представьтесь, чтобы мы знали всех наших героев по именам)', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call:True)
def register(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Фотографии в год открытия')
    item_2 = types.KeyboardButton('Рисунки "Банк будущего"')
    item_3 = types.KeyboardButton('Видео "Взгляд снизу"')
    item_4 = types.KeyboardButton('Фотография с видом из окна офиса')
    item_5 = types.KeyboardButton('Фотографии "До/после"')
    item_6 = types.KeyboardButton('Задать вопрос')
    item_7 = types.KeyboardButton('Контент загружен')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5)
    markup.add(item_6, item_7)
    if call.message:
        if call.data == 'register':
            user_last_command[call.message.chat.id] = 'register'
            bot.send_message(call.message.chat.id, 'Введите ФИО')
        if call.data == 'phone_number':
            user_last_command[call.message.chat.id] = 'phone_number'
            bot.send_message(call.message.chat.id, 'Отправьте сообщением адрес вашей электронной почты')
        if call.data == 'city':
            flag_city_user.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Введите название вашего города')
        if call.data == 'no_email':
            user_last_command[call.message.chat.id] = 'no_email'
            bot.send_message(call.message.chat.id, 'Принято! Пожалуйста, учтите, без вашей почты мы не сможем выслать вам подарок за участие. Если вы не передумали, пожалуйста, выберите контент, которым вам хочется поделиться, чтобы его увидели все участники фестиваля!', reply_markup=markup)


@bot.message_handler(commands=['buttons'])
def buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Фотографии в год открытия')
    item_2 = types.KeyboardButton('Рисунки "Банк будущего"')
    item_3 = types.KeyboardButton('Видео "Взгляд снизу"')
    item_4 = types.KeyboardButton('Фотография с видом из окна офиса')
    item_5 = types.KeyboardButton('Фотографии "До/после"')
    item_6 = types.KeyboardButton('Задать вопрос')
    item_7 = types.KeyboardButton('Контент загружен')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5)
    markup.add(item_6, item_7)
    bot.send_message(message.chat.id,
                     'Выбирай контент, которым тебе хочется поделиться, чтобы его увидели все участники фестиваля!',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def body(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Фотографии в год открытия')
    item_2 = types.KeyboardButton('Рисунки "Банк будущего"')
    item_3 = types.KeyboardButton('Видео "Взгляд снизу"')
    item_4 = types.KeyboardButton('Фотография с видом из окна офиса')
    item_5 = types.KeyboardButton('Фотографии "До/после"')
    item_6 = types.KeyboardButton('Задать вопрос')
    item_7 = types.KeyboardButton('Контент загружен')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5)
    markup.add(item_6, item_7)

    global register_users
    if message.chat.id in user_last_command:
        if user_last_command[message.chat.id] == 'register':
            register_users[str(message.chat.id)] = {}
            register_users[str(message.chat.id)]['user_name'] = message.text
            with open('./users.json', 'w', encoding="utf-8") as f:
                json.dump(register_users, f, ensure_ascii=False)
            if os.path.exists('./users.json'):
                with open('./users.json', 'r', encoding="utf-8") as f:
                    register_users = json.load(f)
            markup_phone_number = types.InlineKeyboardMarkup(row_width=2)
            item_inline_phone = types.InlineKeyboardButton('Указать электронную почту', callback_data='phone_number')
            item_no_email = types.InlineKeyboardButton('Не хочу делиться контактом', callback_data='no_email')
            markup_phone_number.add(item_inline_phone, item_no_email)
            bot.send_message(message.chat.id, 'Очень рады познакомиться!')
            bot.send_message(message.chat.id, 'Пожалуйста, поделитесь своей почтой, чтобы мы ни в коем случае не потерялись', reply_markup=markup_phone_number)
            del user_last_command[message.chat.id]
        elif user_last_command[message.chat.id] == 'phone_number':
            register_users[str(message.chat.id)]['phone_number'] = message.text
            with open('./users.json', 'w', encoding="utf-8") as f:
                json.dump(register_users, f, ensure_ascii=False)
            if os.path.exists('./users.json'):
                with open('./users.json', 'r', encoding="utf-8") as f:
                    register_users = json.load(f)
            bot.send_message(message.chat.id, 'Спасибо! Теперь, пожалуйста, выберите контент, которым вам хочется поделиться, чтобы его увидели все участники фестиваля! ', reply_markup=markup)
            del user_last_command[message.chat.id]
        elif user_last_command[message.chat.id] == 'no_email':
            print('ок')
            register_users[str(message.chat.id)]['phone_number'] = '-'
            with open('./users.json', 'w', encoding="utf-8") as f:
                json.dump(register_users, f, ensure_ascii=False)
            if os.path.exists('./users.json'):
                with open('./users.json', 'r', encoding="utf-8") as f:
                    register_users = json.load(f)


    if message.chat.id in flag_city_user:
        city_user[message.chat.id] = message.text
        bot.send_message(message.chat.id, 'Город добавлен')
        bot.send_message(message.chat.id, 'Отправляйте фото')

    markup_inline_city = types.InlineKeyboardMarkup(row_width=1)
    item_inline_city = types.InlineKeyboardButton('Указать свой город', callback_data='city')
    markup_inline_city.add(item_inline_city)

    if message.text == 'Фотографии в год открытия':
        bot.send_message(message.chat.id, '1996 год. В России открывается первое отделение Райффайзен Банк, а чем вы занимаетесь в 1996? Уже работаете и развиваете свои профессиональные навыки? Или учитесь в Университете и готовитесь к защите диплома? Может, вы еще в школе, выбираете свое будущее и мечтаете стать космонавтом? Или вы – тот самый милый малыш у новогодней елки в детском саду? Найдите свое фото из 1996 года, отсканируйте или сфотографируйте на телефон и пришлите его, пожалуйста, нам)')
        user_last_command[message.chat.id] = 'photo_in_the_opening_year'


    elif message.text == 'Рисунки "Банк будущего"':
        bot.send_message(message.chat.id, 'Спорим, ваш ребенок – очень талантливый художник с безграничной фантазией? Докажите это всем! Вот вам и вашему юному таланту небольшое домашнее задание: нарисовать рисунок на тему “Райффайзен Банк будущего”. Никаких ограничений по техникам, масштабам и форматам)')
        user_last_command[message.chat.id] = 'drawings_bank_future'

    elif message.text == 'Видео "Взгляд снизу"':
        bot.send_message(message.chat.id, 'У вас есть дети? Они точно знают, где вы работаете? Давайте снимем с ними небольшое интервью в стиле “Взгляд снизу”. Будет идеально, если ваше видео будет снято горизонтально, с хорошим светом и звуком.')
        user_last_command[message.chat.id] = 'video_view_bottom'


    elif message.text == 'Фотография с видом из окна офиса':
        bot.send_message(message.chat.id, 'За 26 лет география офисов Райффайзен Банк разрослась по всей России! Пришлите фото с видом из окна вашего офиса, у нас будет захватывающая игра, в которой будет и ваше фото) Но, первым делом, до отправки фото, обязательно укажите город!', reply_markup=markup_inline_city)
        user_last_command[message.chat.id] = 'photo_view_from_office_window'
    elif message.text == 'Фотографии "До/после"':
        bot.send_message(message.chat.id, 'Признайтесь, вам нравится смотреть подборки «Было/Стало» или «До/После») Покажите и вы нам, какой путь вы прошли и как изменились за 26 лет! Пришлите нам две свои фотографии: из 1996 и 2022 года, а мы превратим это в интерактивную фотогалерею на Values Fest 2022!')
        user_last_command[message.chat.id] = 'photo_before_after'
    elif message.text == 'Задать вопрос':
        bot.send_message(message.chat.id, 'Перейдите по ссылке в чат с модератором и задайте интересующий вас вопрос')
        bot.send_message(message.chat.id, MODERATOR_CHAT_LINK)
    elif message.text == 'Контент загружен':
        bot.send_message(message.chat.id, 'Огромное спасибо и до скорой встречи на Фестивале ValuesFest 2022!')




@bot.message_handler(content_types=['photo', 'video', 'document'])
def body_content(message):
    global file_info
    count = 1
    city = ''
    if message.chat.id in city_user:
        city = city_user[message.chat.id]
        del city_user[message.chat.id]
        flag_city_user.remove(message.chat.id)
    else:
        city = ''

    if message.media_group_id != None and not(message.chat.id in group_photo):
        count = 2
        group_photo[message.chat.id] = 2

    if str(message.chat.id) in register_users:
        user_name = register_users[str(message.chat.id)]['user_name']
        phone_number = register_users[str(message.chat.id)]['phone_number']
    else:
        user_name = f'{message.from_user.last_name} {message.from_user.first_name}'
        phone_number = '-'

    if message.photo:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_name = file_info.file_path.split('/')[-1]
    elif message.document:
        file_info = file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
    elif message.video:
        try:
            file_info = bot.get_file(message.video.file_id)
            file_name = file_info.file_path.split('/')[-1]
        except:
            file_name = user_name
            bot.send_message(ADMIN_ID, f'пользователь: {user_name} отправил слишком большое видео. Телефон: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)

    if message.chat.id in user_last_command:
        writing_file_to_server(message, user_last_command[message.chat.id], count=count, file_name=file_name, file_info=file_info, user_name=user_name, phone_number=phone_number)
        add_row_for_csv_file(user_name=user_name, dir=user_last_command[message.chat.id], name_file=file_name,
                             link_for_file=f'./{user_last_command[message.chat.id]}/{file_name}', phone_number=phone_number, city=city)

        upload_to_folder(real_folder_id=id_dir_on_drive[user_last_command[message.chat.id]],
                         file_for_load=f'./files/{user_last_command[message.chat.id]}/{file_name}', file_name=file_name,
                         user_name=user_name, phone_number=phone_number, city=city)
        shutil.make_archive('files_archive', 'zip', './files')
        if message.chat.id in group_photo:
            group_photo[message.chat.id] = group_photo[message.chat.id] - 1

        if message.chat.id in group_photo:
            if (message.chat.id in user_last_command) and group_photo[message.chat.id] == 0:
                del user_last_command[message.chat.id]
                del group_photo[message.chat.id]


    else:
        bot.send_message(message.chat.id, 'Перед отправкой файла нужно выбрать тип контента. Воспользуйтесь клавиатурой, чтобы выбрать, чем Вы хотите поделиться. После этого отправьте файл повторно.')

if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
