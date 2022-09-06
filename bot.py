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

data_for_table ={}
question_command = {}

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
                             f'пользователь: {user_name} отправил видео. Почта: {phone_number}')
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
                             f'пользователь: {user_name} отправил фото {type_dir}. Почта: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    elif type_dir == 'photo_in_the_opening_year':
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'./files/photo_in_the_opening_year/{file_name}', 'wb') as f:
                f.write(downloaded_file)

        except Exception as e:
            print('ошибка загрузки фото', e)
            bot.send_message(message.chat.id, 'ошибка загрузки фото')
            bot.send_message(ADMIN_ID,
                             f'пользователь: {user_name} отправил фото {type_dir}. Почта: {phone_number}')
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
                             f'пользователь: {user_name} отправил фото {type_dir}. Почта: {phone_number}')
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
                             f'пользователь: {user_name} отправил фото {type_dir}. Почта: {phone_number}')
            bot.copy_message(ADMIN_ID, message.chat.id, message.id)
    if count == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_1 = types.KeyboardButton('Фотографии в период с 1996 по 2000 год')
        item_2 = types.KeyboardButton('Рисунки «Райффайзен Банк будущего»')
        item_3 = types.KeyboardButton('Видео «Взгляд снизу»')
        item_4 = types.KeyboardButton('Фотография с видом из окна вашего офиса')
        item_5 = types.KeyboardButton(' Фотографии «Райф. Лучшие моменты»')
        item_6 = types.KeyboardButton('Задать вопрос')
        item_7 = types.KeyboardButton('Контент загружен')
        markup.add(item_1, item_2)
        markup.add(item_3, item_4)
        markup.add(item_5)
        markup.add(item_6, item_7)
        bot.send_message(message.chat.id, '''Спасибо, что поделились своей историей.
Информацию о подарках и победителях вы узнаете в финальный день фестиваля на платформе.
Проверьте, что загрузили весь контент по заданиям, в которых участвуете. Если нет — сначала закончите задания. 
Если контент загружен полностью — нажмите на кнопку «Контент загружен».
''', reply_markup=markup)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    item_inline_1 = types.InlineKeyboardButton('Регистрация', callback_data='register')
    markup_inline.add(item_inline_1)
    bot.send_message(message.chat.id, '''Привет!
Спасибо, что решили поучаствовать в создании Values Fest 2022.
Чтобы наполнить фестиваль эмоциями и сделать его по-настоящему живым, предлагаем вам присоединиться к его подготовке. Выбирайте задания из списка (обещаем, ничего сложного не будет!) и присылайте ваши фото- и видеоистории.  
Главное — успеть до конца дня 16 сентября. 

Если у вас возникнут вопросы — задайте их @valuesfestsupport или напишите /start, чтобы перезапустить бот.
Теперь, если вы готовы начать, пожалуйста, представьтесь, чтобы мы знали всех наших героев по именам.
''', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def register(call):
    #клавиатура для год открытия
    markup_inline_year_2 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_year_3 = types.InlineKeyboardMarkup(row_width=1)
    item_inline_year_2 = types.InlineKeyboardButton('Далее', callback_data='question_2')
    item_inline_year_3 = types.InlineKeyboardButton('Далее', callback_data='question_3')
    markup_inline_year_2.add(item_inline_year_2)
    markup_inline_year_3.add(item_inline_year_3)
    #клавиатура для рисунка
    markup_inline_bank_2 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_bank_3 = types.InlineKeyboardMarkup(row_width=1)
    item_inline_bank_2 = types.InlineKeyboardButton('Далее', callback_data='age')
    item_inline_bank_3 = types.InlineKeyboardButton('Далее', callback_data='job_title')
    markup_inline_bank_2.add(item_inline_bank_2)
    markup_inline_bank_3.add(item_inline_bank_3)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Фотографии в период с 1996 по 2000 год')
    item_2 = types.KeyboardButton('Рисунки «Райффайзен Банк будущего»')
    item_3 = types.KeyboardButton('Видео «Взгляд снизу»')
    item_4 = types.KeyboardButton('Фотография с видом из окна вашего офиса')
    item_5 = types.KeyboardButton(' Фотографии «Райф. Лучшие моменты»')
    item_6 = types.KeyboardButton('Задать вопрос')
    item_7 = types.KeyboardButton('Контент загружен')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5)
    markup.add(item_6, item_7)
    if call.message:
        if call.data == 'register':
            user_last_command[call.message.chat.id] = 'register'
            bot.send_message(call.message.chat.id, 'Введите ваши фамилию и имя')
        if call.data == 'phone_number':
            user_last_command[call.message.chat.id] = 'phone_number'
            bot.send_message(call.message.chat.id, 'Отправьте сообщением адрес вашей электронной почты')
        if call.data == 'city':
            flag_city_user.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Укажите город, чтобы мы знали правильный ответ.')
        if call.data == 'no_email':
            user_last_command[call.message.chat.id] = 'no_email'
            bot.send_message(call.message.chat.id, '''Нам важно знать создателей фестиваля в лицо :)

Если вам некомфортно общаться в Телеграме и оставлять здесь свой контакт, вы можете написать нам в Слаке в аккаунт Values Fest Content или по адресу электронной почты support@zeenevents.com.

Если вы все же решите поделиться контентом с помощью бота, пожалуйста, перезапустите его, написав /start, и мы начнем сначала.
''', reply_markup=markup)
        if call.data == 'question_1':
            question_command[call.message.chat.id] = 'question_1'
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, год, в который была сделана ваша фотография.')

            if not (call.message.chat.id  in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'question_2':
            question_command[call.message.chat.id] = 'question_2'
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, кем вы были в этот год.')
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'question_3':
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, какую должность сейчас вы занимаете в Райффайзен Банке.')
            question_command[call.message.chat.id] = 'question_3'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'name_child':
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, имя ребенка.')
            question_command[call.message.chat.id] = 'name_child'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'age':
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, возраст ребенка.')
            question_command[call.message.chat.id] = 'age'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'job_title':
            bot.send_message(call.message.chat.id, 'Сообщите, пожалуйста, на какой позиции вы работаете в банке.')
            question_command[call.message.chat.id] = 'job_title'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'name_child_new':
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, имя ребенка.')
            question_command[call.message.chat.id] = 'name_child_new'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'last_name':
            bot.send_message(call.message.chat.id, 'Укажите, пожалуйста, фамилию ребенка.')
            question_command[call.message.chat.id] = 'last_name'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'job_title_new':
            bot.send_message(call.message.chat.id, 'Сообщите, пожалуйста, на какой позиции вы работаете в банке.')
            question_command[call.message.chat.id] = 'job_title_new'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}
        if call.data == 'description':
            bot.send_message(call.message.chat.id, 'Добавьте описание, чтобы участники фестиваля смогли проникнуться дорогими для вас воспоминаниями.')
            question_command[call.message.chat.id] = 'description'
            if not (call.message.chat.id in data_for_table):
                data_for_table[call.message.chat.id] = {}




@bot.message_handler(commands=['buttons'])
def buttons(message):
    bot.send_message(message.chat.id, '''<b>сообщение</b> !другой _текст_

текст после пустой строки''', parse_mode='HTML')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Фотографии в период с 1996 по 2000 год')
    item_2 = types.KeyboardButton('Рисунки «Райффайзен Банк будущего»')
    item_3 = types.KeyboardButton('Видео «Взгляд снизу»')
    item_4 = types.KeyboardButton('Фотография с видом из окна вашего офиса')
    item_5 = types.KeyboardButton(' Фотографии «Райф. Лучшие моменты»')
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
    item_1 = types.KeyboardButton('Фотографии в период с 1996 по 2000 год')
    item_2 = types.KeyboardButton('Рисунки «Райффайзен Банк будущего»')
    item_3 = types.KeyboardButton('Видео «Взгляд снизу»')
    item_4 = types.KeyboardButton('Фотография с видом из окна вашего офиса')
    item_5 = types.KeyboardButton(' Фотографии «Райф. Лучшие моменты»')
    item_6 = types.KeyboardButton('Задать вопрос')
    item_7 = types.KeyboardButton('Контент загружен')
    markup.add(item_1, item_2)
    markup.add(item_3, item_4)
    markup.add(item_5)
    markup.add(item_6, item_7)
    #клавиатура для год открытия
    markup_inline_year_1 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_year_2 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_year_3 = types.InlineKeyboardMarkup(row_width=1)
    item_inline_year_1 = types.InlineKeyboardButton('Начать', callback_data='question_1')
    item_inline_year_2 = types.InlineKeyboardButton('Далее', callback_data='question_2')
    item_inline_year_3 = types.InlineKeyboardButton('Далее', callback_data='question_3')
    markup_inline_year_1.add(item_inline_year_1)
    markup_inline_year_2.add(item_inline_year_2)
    markup_inline_year_3.add(item_inline_year_3)

    # клавиатура для рисунка
    markup_inline_bank_1 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_bank_2 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_bank_3 = types.InlineKeyboardMarkup(row_width=1)
    item_inline_bank_2 = types.InlineKeyboardButton('Далее', callback_data='age')
    item_inline_bank_3 = types.InlineKeyboardButton('Далее', callback_data='job_title')
    item_inline_bank_1 = types.InlineKeyboardButton('Начать', callback_data='name_child')
    markup_inline_bank_1.add(item_inline_bank_1)
    markup_inline_bank_2.add(item_inline_bank_2)
    markup_inline_bank_3.add(item_inline_bank_3)

    # клавиатура видео
    markup_inline_video_1 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_video_2 = types.InlineKeyboardMarkup(row_width=1)
    markup_inline_video_3 = types.InlineKeyboardMarkup(row_width=1)
    item_inline_video_1 = types.InlineKeyboardButton('Начать', callback_data='name_child_new')
    item_inline_video_2 = types.InlineKeyboardButton('Далее', callback_data='last_name')
    item_inline_video_3 = types.InlineKeyboardButton('Далее', callback_data='job_title_new')
    markup_inline_video_1.add(item_inline_video_1)
    markup_inline_video_2.add(item_inline_video_2)
    markup_inline_video_3.add(item_inline_video_3)
    # клавиатура моменты банка
    markup_inline_moment = types.InlineKeyboardMarkup(row_width=1)
    item_inline_moment_1 = types.InlineKeyboardButton('Начать', callback_data='description')
    markup_inline_moment.add(item_inline_moment_1)

    if message.chat.id in question_command:
        if question_command[message.chat.id] == 'question_1':
            bot.send_message(message.chat.id, 'Данные добавлены', reply_markup=markup_inline_year_2)
        if question_command[message.chat.id] == 'question_2':
            bot.send_message(message.chat.id, 'Данные добавлены', reply_markup=markup_inline_year_3)
        if question_command[message.chat.id] == 'name_child':
            bot.send_message(message.chat.id, 'Данные добавлены', reply_markup=markup_inline_bank_2)
        if question_command[message.chat.id] == 'age':
            bot.send_message(message.chat.id, 'Данные добавлены', reply_markup=markup_inline_bank_3)
        if question_command[message.chat.id] == 'name_child_new':
            bot.send_message(message.chat.id, 'Данные добавлены', reply_markup=markup_inline_video_2)
        if question_command[message.chat.id] == 'last_name':
            bot.send_message(message.chat.id, 'Данные добавлены', reply_markup=markup_inline_video_3)


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
            bot.send_message(message.chat.id, '''Рады познакомиться.
Пожалуйста, поделитесь своей корпоративной почтой, чтобы мы могли с вами связаться.''', reply_markup=markup_phone_number)
            del user_last_command[message.chat.id]
        elif user_last_command[message.chat.id] == 'phone_number':
            register_users[str(message.chat.id)]['phone_number'] = message.text
            with open('./users.json', 'w', encoding="utf-8") as f:
                json.dump(register_users, f, ensure_ascii=False)
            if os.path.exists('./users.json'):
                with open('./users.json', 'r', encoding="utf-8") as f:
                    register_users = json.load(f)
            bot.send_message(message.chat.id, '''Спасибо.
Вот краткое описание заданий. Подробнее — по кнопке в каждой категории.

<b><ins>Фото в период в период с 1996 по 2000 год.</ins></b> Покажите нам, какими вы были: работали, еще учились или даже ходили в детский сад?
<b><ins>Видео «Взгляд снизу».</ins></b> Снимите видеоинтервью с вашим ребенком о работе в банке.
<b><ins> Фотографии «Райф. Лучшие моменты».</ins></b> Присылайте фото из ваших архивов с самыми яркими, теплыми и веселыми воспоминаниями с коллегами.
<b><ins>Рисунки «Райффайзен Банк будущего».</ins></b> Покажите, как видят ваши дети наш банк в будущем.
<b><ins>Фото с видом из окна.</ins></b> Присылайте фото с видом из окна офиса или дома, если работаете удаленно.

Вы можете нажать на кнопку, чтобы получить более подробную информацию по каждой из активностей.
Когда будете готовы, нажмите кнопку в нужной категории повторно и загрузите контент.
Вашу историю увидит каждый участник Values Fest 2022.
''', reply_markup=markup, parse_mode='HTML')
            del user_last_command[message.chat.id]
        elif user_last_command[message.chat.id] == 'no_email':
            register_users[str(message.chat.id)]['phone_number'] = '-'
            with open('./users.json', 'w', encoding="utf-8") as f:
                json.dump(register_users, f, ensure_ascii=False)
            if os.path.exists('./users.json'):
                with open('./users.json', 'r', encoding="utf-8") as f:
                    register_users = json.load(f)

    if message.chat.id in flag_city_user:
        city_user[message.chat.id] = message.text
        bot.send_message(message.chat.id, 'Спасибо, теперь загрузите фото.')
    # клавиатура для города
    markup_inline_city = types.InlineKeyboardMarkup(row_width=1)
    item_inline_city = types.InlineKeyboardButton('Начать', callback_data='city')
    markup_inline_city.add(item_inline_city)



    if message.text == 'Фотографии в период с 1996 по 2000 год':
        bot.send_message(message.chat.id, '''1996 год. Райффайзен Банк приходит в Россию и делает первые, но уверенные шаги на рынке, а чем занимаетесь в это время вы? Уже работаете и развиваете свои профессиональные навыки? Или учитесь в университете и готовитесь к защите диплома? Может, вы еще в школе, выбираете свое будущее и мечтаете о времени без домашних заданий, контрольных и экзаменов? Или рассказываете стихи на утреннике в детском саду? Пожалуйста, найдите свое фото в период с 1996 по 2000 год, отсканируйте или сфотографируйте на телефон и пришлите нам.
Ваши коллеги смогут оценить фото, а вы получите шанс выиграть подарок.
Перед загрузкой фото, пожалуйста, ответьте на несколько вопросов.''', reply_markup=markup_inline_year_1)
        user_last_command[message.chat.id] = 'photo_in_the_opening_year'


    elif message.text == 'Рисунки «Райффайзен Банк будущего»':
        bot.send_message(message.chat.id,
                         '''Пикассо считал, что каждый ребенок — художник. Мы согласны с мастером и приготовили небольшое задание для маленьких гениев — изобразить Райффайзен Банк будущего. Никаких ограничений по технике, масштабу и формату нет. Скан или фото рисунка пришлите, пожалуйста, нам. 
Перед загрузкой фото, пожалуйста, ответьте на несколько вопросов.
''', reply_markup=markup_inline_bank_1)
        user_last_command[message.chat.id] = 'drawings_bank_future'
    elif message.text == 'Видео «Взгляд снизу»':
        bot.send_message(message.chat.id, '''У вас есть дети? Они точно знают, где вы работаете? Снимите небольшое интервью с вашим ребенком. Для авторов роликов с самыми креативными и искренними ответами мы приготовили подарки. Победителей определим голосованием. 
Чтобы все разглядели и услышали наших маленьких героев, видео снимайте горизонтально, с хорошим светом и звуком. На видео должен быть только ребенок.

<b>Вопросы для интервью</b>
1.Где работает мама (или папа)?
2.Чем мама (или папа) занимается на работе? А чем занимаются банковские работники?
3.Что такое ценность? 
4.Что для тебя самое ценное?
5.Выберите одну из пяти ценностей: проактивность, саморазвитие, профессионализм, ответственность, сотрудничество — и спросите о ней ребенка. Как ты думаешь, что это такое?
6.Что происходит с людьми, которых отправляют на удаленку?

Перед загрузкой видео, пожалуйста, ответьте на несколько вопросов.
''', parse_mode='HTML', reply_markup=markup_inline_video_1)
        user_last_command[message.chat.id] = 'video_view_bottom'


    elif message.text == 'Фотография с видом из окна вашего офиса':
        bot.send_message(message.chat.id, '''За 26 лет Райффайзен Банк открыл офисы по всей территории России. Давайте проверим, смогут ли коллеги угадать ваш город, а вы — их. Присылайте фото с видом из окна офиса или дома, если работаете удаленно. 
Перед загрузкой фото, пожалуйста, ответьте на вопрос.
''', reply_markup=markup_inline_city)
        user_last_command[message.chat.id] = 'photo_view_from_office_window'
    elif message.text == 'Фотографии «Райф. Лучшие моменты»':
        bot.send_message(message.chat.id, '''Мы верим, что Райффайзен Банк — не просто место работы, это еще и источник теплых воспоминаний и радостных моментов. Пришлите нам фотографию дня рождения, корпоративного мероприятия или другого приятного события, которое вы разделили с коллегами. 
Перед загрузкой, пожалуйста, добавьте информацию о фото.
''', reply_markup=markup_inline_moment)
        user_last_command[message.chat.id] = 'photo_before_after'

    elif message.text == 'Задать вопрос':
        bot.send_message(message.chat.id, '''Чтобы задать вопрос, перейдите в чат с модератором — @valuesfestsupport.''')
        bot.send_message(message.chat.id, MODERATOR_CHAT_LINK)
    elif message.text == 'Контент загружен':
        bot.send_message(message.chat.id, 'Спасибо и до скорой встречи на Values Fest 2022.')

    if message.chat.id in question_command:
        if question_command[message.chat.id] == 'question_1':
            data_for_table[message.chat.id]['question_1'] = message.text
        if question_command[message.chat.id] == 'question_2':
            data_for_table[message.chat.id]['question_2'] = message.text
        if question_command[message.chat.id] == 'question_3':
            data_for_table[message.chat.id]['question_3'] = message.text
            bot.send_message(message.chat.id, 'Спасибо, теперь загрузите фото.')
            question_command[message.chat.id] = ''
        if question_command[message.chat.id] == 'name_child':
            data_for_table[message.chat.id]['name_child'] = message.text
        if question_command[message.chat.id] == 'age':
            data_for_table[message.chat.id]['age'] = message.text
        if question_command[message.chat.id] == 'job_title':
            data_for_table[message.chat.id]['job_title'] = message.text
            bot.send_message(message.chat.id, 'Спасибо, теперь загрузите фото.')
            question_command[message.chat.id] = ''
        if question_command[message.chat.id] == 'name_child_new':
            data_for_table[message.chat.id]['name_child_new'] = message.text
        if question_command[message.chat.id] == 'last_name':
            data_for_table[message.chat.id]['last_name'] = message.text
        if question_command[message.chat.id] == 'job_title_new':
            data_for_table[message.chat.id]['job_title_new'] = message.text
            bot.send_message(message.chat.id, 'Спасибо, теперь загрузите видео.')
            question_command[message.chat.id] = ''
        if question_command[message.chat.id] == 'description':
            data_for_table[message.chat.id]['description'] = message.text
            bot.send_message(message.chat.id, 'Спасибо, теперь загрузите фото.')
            question_command[message.chat.id] = ''




@bot.message_handler(content_types=['photo', 'video', 'document'])
def body_content(message):
    global file_info
    count = 1
    city = ''
    if str(message.chat.id) in register_users:

        if message.chat.id in city_user:
            city = city_user[message.chat.id]
            del city_user[message.chat.id]
            flag_city_user.remove(message.chat.id)
        else:
            city = ''

        if message.media_group_id != None and not (message.chat.id in group_photo):
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
                bot.send_message(ADMIN_ID,
                                 f'пользователь: {user_name} отправил слишком большое видео. Почта: {phone_number}')
                bot.copy_message(ADMIN_ID, message.chat.id, message.id)

        if message.chat.id in user_last_command:
            writing_file_to_server(message, user_last_command[message.chat.id], count=count, file_name=file_name,
                                   file_info=file_info, user_name=user_name, phone_number=phone_number)
            add_row_for_csv_file(user_name=user_name, dir=user_last_command[message.chat.id], name_file=file_name,
                                 link_for_file=f'./{user_last_command[message.chat.id]}/{file_name}',
                                 phone_number=phone_number, city=city, chat_id=message.chat.id, data_for_table=data_for_table)

            upload_to_folder(real_folder_id=id_dir_on_drive[user_last_command[message.chat.id]],
                             file_for_load=f'./files/{user_last_command[message.chat.id]}/{file_name}',
                             file_name=file_name,
                             user_name=user_name, phone_number=phone_number, city=city, chat_id=message.chat.id, data_for_table=data_for_table)
            shutil.make_archive('files_archive', 'zip', './files')
            question_command[message.chat.id] = ''
            if message.chat.id in group_photo:
                group_photo[message.chat.id] = group_photo[message.chat.id] - 1

            if message.chat.id in group_photo:
                if (message.chat.id in user_last_command) and group_photo[message.chat.id] == 0:
                    del user_last_command[message.chat.id]
                    del group_photo[message.chat.id]

        else:
            bot.send_message(message.chat.id,
                             'Перед отправкой файла нужно выбрать тип контента. Воспользуйтесь клавиатурой, чтобы выбрать, чем Вы хотите поделиться. После этого отправьте файл повторно.')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста зарегистрируйтесь, прежде чем отправлять контент')
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        item_inline_1 = types.InlineKeyboardButton('Регистрация', callback_data='register')
        markup_inline.add(item_inline_1)
        bot.send_message(message.chat.id,
                         'Привет! Спасибо, что решили поучаствовать в создании Values Fest 2022! Пожалуйста, представьтесь, чтобы мы знали всех наших героев по именам)',
                         reply_markup=markup_inline)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)