import os.path
import csv
from settings import ADMIN_ID

#формирование csv докумената и добавление записей
#//////////////////////////////////////////////////////////
def past_link(text, link):
    rusult = f'=ГИПЕРССЫЛКА("{link}"; "{text}")'
    return rusult


def add_row_for_csv_file(user_name, dir, name_file, link_for_file, phone_number, city, question_1='', question_2='', question_3='', name_age='', job_title='', description='', last_name=''):
    if not os.path.exists('./files/data.csv'):
        headlines = ['пользователь', 'Фотографии в год открытия', 'Рисунки "Банк будущего"', 'Видео "Взгляд снизу"', 'Фотография с видом из окна офиса', 'Фотографии "До/после"','Контактный телефон ', 'Город', 'Год', 'Тогда', 'Сейчас']
        with open('files/data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(headlines)

    if dir == 'photo_in_the_opening_year':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, past_link(name_file, link_for_file),'','','','', phone_number, city, question_1, question_2, question_3))
    if dir == 'drawings_bank_future':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', past_link(name_file, link_for_file), '','','', phone_number, city,'','','', name_age, job_title))
    if dir == 'video_view_bottom':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', past_link(name_file, link_for_file), '','', phone_number, city,'','','', '', job_title, '', last_name))
    if dir == 'photo_view_from_office_window':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', '', past_link(name_file, link_for_file), '', phone_number,city))
    if dir == 'photo_before_after':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', '', '', past_link(name_file, link_for_file), phone_number, city,  '', '','', '','', description))
#//////////////////////////////////////////////////////////////
