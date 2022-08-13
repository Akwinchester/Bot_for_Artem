import os.path
import csv
from google_sheets import GoogleSheet
from settings import ADMIN_ID

#формирование csv докумената и добавление записей
#//////////////////////////////////////////////////////////
def past_link(text, link):
    rusult = f'=ГИПЕРССЫЛКА("{link}"; "{text}")'
    return rusult


def add_row_for_csv_file(user_name, type_file, name_file, link_for_file):
    if not os.path.exists('files/data.csv'):
        headlines = ['пользователь','фото', 'текст', 'видео', 'аудио']
        with open('files/data.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(headlines)

    if type_file == 'photo':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, past_link(name_file, link_for_file)))
    if type_file == 'document':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', past_link(name_file, link_for_file)))
    if type_file == 'video':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', past_link(name_file, link_for_file)))
    if type_file == 'audio':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', '', past_link(name_file, link_for_file)))
#//////////////////////////////////////////////////////////////


#запись файла на сервер



#//////////////////////////////////////////////////////////////
#работа с google sheets
#//////////////////////////////////////////////////////////////
def add_row_for_google_sheets(user_name, type_file, name_file, link_for_file):
    if type_file == 'photl':
        pass
#//////////////////////////////////////////////////////////////