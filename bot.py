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

if os.path.exists('./users.json'):
    with open('./users.json', 'r', encoding="utf-8") as f:
        register_users = json.load(f)


def writing_file_to_server(message, type_dir, count, file_name=None):
    if type_dir == 'video_view_bottom':
        try:
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/video_view_bottom/{file_name}', 'wb') as f:
                f.write(downloaded_file)
        except:
            print('ошибка загрузки видео')
            bot.send_message(message.chat.id, 'ошибка загрузки видео')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir == 'photo_view_from_office_window':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_view_from_office_window/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir== 'photo_in_the_opening_year':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_in_the_opening_year/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except Exception as e:
            print('ошибка загрузки фото', e)
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir == 'drawings_bank_future':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/drawings_bank_future/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    elif type_dir == 'photo_before_after':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_before_after/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except:
            print('ошибка загрузки фото')
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.copy_message(ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    if count == 1:
        bot.send_message(message.chat.id, 'Спасибо ! Еще немного и ты увидишь насколько ярче и интересней станет ValuesFest 2022 благодаря тебе! Проверь остальные категории, может, есть еще что-то интересное, чем ты еще не поделился?)')


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

    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    item_inline_1 = types.InlineKeyboardButton('Регистрация', callback_data='register')
    item_inline_2 = types.InlineKeyboardButton('Указать контактный телефон', callback_data='phone_number')
    markup_inline.add(item_inline_1, item_inline_2)
    bot.send_message(message.chat.id, '''Привет! 
Спасибо, что решил поучаствовать в создании Values Fest 2022! 
Пожалуйста, представься, чтобы мы знали всех наших героев по именам)'''
, reply_markup=markup_inline)

#     bot.send_message(message.chat.id, f'''Отправь мне такое сообщение
# ригистрация:ФИО''')

@bot.callback_query_handler(func=lambda call:True)
def register(call):
    if call.message:
        if call.data == 'register':
            user_last_command[call.message.chat.id] = 'register'
            bot.send_message(call.message.chat.id, 'Введите ФИО')
        if call.data == 'phone_number':
            user_last_command[call.message.chat.id] = 'phone_number'
            bot.send_message(call.message.chat.id, 'Введите номер телефона в формате: 8**********. Разделители указывать не нужно')


@bot.message_handler(content_types=['text'])
def body(message):
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

            bot.send_message(message.chat.id, '''Очень рады познакомиться! Нажми на кнопку "Указать контактный телефон" под предыдущем сообщением.''')
        if user_last_command[message.chat.id] == 'phone_number':
            register_users[str(message.chat.id)]['phone_number'] = message.text
            bot.send_message(message.chat.id, 'Номер сохранен')
            bot.send_message(message.chat.id, 'Выбирай контент, которым тебе хочется поделиться, чтобы его увидели все участники фестиваля!')
            with open('./users.json', 'w', encoding="utf-8") as f:
                json.dump(register_users, f, ensure_ascii=False)
            if os.path.exists('./users.json'):
                with open('./users.json', 'r', encoding="utf-8") as f:
                    register_users = json.load(f)
        del user_last_command[message.chat.id]

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
        bot.send_message(message.chat.id, 'Перейдите по ссылке в чат с модератором и задайте интересующий Вас вопрос')
        bot.send_message(message.chat.id, MODERATOR_CHAT_LINK)




@bot.message_handler(content_types=['photo', 'video'])
def body_content(message):
    count = 1
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
    elif message.video:
        try:
            file_info = bot.get_file(message.video.file_id)
            file_name = file_info.file_path.split('/')[-1]
        except:
            file_name = user_name
            bot.send_message(ADMIN_ID, f'пользователь {user_name} отправил слишком большое видео')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)

    if message.chat.id in user_last_command:
        writing_file_to_server(message, user_last_command[message.chat.id], count=count, file_name=file_name)
        add_row_for_csv_file(user_name=user_name, dir=user_last_command[message.chat.id], name_file=file_name,
                             link_for_file=f'./{user_last_command[message.chat.id]}/{file_name}', phone_number=phone_number)
        upload_to_folder(real_folder_id=id_dir_on_drive[user_last_command[message.chat.id]],
                         file_for_load=f'./files/{user_last_command[message.chat.id]}/{file_name}', file_name=file_name,
                         user_name=user_name)
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
