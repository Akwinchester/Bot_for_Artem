import telebot
from telebot import types
import wget
from .settings import tn



bot = telebot.TeleBot(tn)

def download(url):
    wget.download(url)


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
    if message.text == 'Текст':
        bot.send_message(message.chat.id, 'Отправте текстовый документ')
    elif message.text == 'Фото':
        bot.send_message(message.chat.id, 'Отправьте фото')
    elif message.text == 'Видео':
        bot.send_message(message.chat.id, 'Отправьте видео')
    elif message.text == 'Аудио':
        bot.send_message(message.chat.id, 'Отправьте аудиофайл')

    if message.photo:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'./files/{file_info.file_path}', 'wb') as f:
            f.write(downloaded_file)

        bot.send_message(message.chat.id, 'фото загружено')

    elif message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'./files/documents/{message.document.file_name}', 'wb') as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id, 'документ загружен')

    elif message.audio:
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        print(file_info.file_path)
        with open(f'./files/{file_info.file_path}', 'wb') as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id, 'аудиофайл загружен')

    elif message.video:
        file_info = bot.get_file(message.video.file_id)
        print(1)
        downloaded_file = bot.download_file(file_info.file_path)
        print(file_info.file_path)
        with open(f'./files/{file_info.file_path}', 'wb') as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id, 'видео загружено')

if __name__ == '__main__':
    bot.polling(none_stop=True)