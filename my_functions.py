import os.path
import csv
from google_sheets import GoogleSheet
from settings import ADMIN_ID

#формирование csv докумената и добавление записей
#//////////////////////////////////////////////////////////
def past_link(text, link):
    rusult = f'=ГИПЕРССЫЛКА("{link}"; "{text}")'
    return rusult


def add_row_for_csv_file(user_name, dir, name_file, link_for_file):
    if not os.path.exists('files/data.csv'):
        headlines = ['пользователь', 'Фотографии в год открытия', 'Рисунки "Банк будущего"', 'Видео "Взгляд снизу"', 'Фотография с видом из окна офиса']
        with open('files/data.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(headlines)

    if dir == 'photo_in_the_opening_year':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, past_link(name_file, link_for_file)))
    if dir == 'drawings_bank_future':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', past_link(name_file, link_for_file)))
    if dir == 'video_view_bottom':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', past_link(name_file, link_for_file)))
    if dir == 'photo_view_from_office_window':
        with open('files/data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', '', past_link(name_file, link_for_file)))
#//////////////////////////////////////////////////////////////


#работа с google sheets
#//////////////////////////////////////////////////////////////
def add_row_for_google_sheets(user_name, type_file, name_file, link_for_file):
    if type_file == 'photl':
        pass
#//////////////////////////////////////////////////////////////