import os.path
import csv
from settings import ADMIN_ID

#формирование csv докумената и добавление записей
#//////////////////////////////////////////////////////////
def past_link(text, link):
    rusult = f'=ГИПЕРССЫЛКА("{link}"; "{text}")'
    return rusult


def add_row_for_csv_file(user_name, dir, name_file, link_for_file, phone_number, city, chat_id, data_for_table={}):
    if not os.path.exists('./files/data.csv'):
        headlines = ['Пользователь',	'Фотографии в год открытия',	'Рисунки "Банк будущего"',	'Видео "Взгляд снизу"',	'Фотография с видом из окна офиса',	'Фотографии "Моменты Райффайзен Банк Будущего"', 'Почта',	'Город',	'Год',	'Тогда',	'Должность сейчас',	'Имя ребенка',	'Возраст ребенка', 	'Фамилия ребенка',	'Описание']
        with open('files/data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(headlines)

    if dir == 'photo_in_the_opening_year':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, past_link(name_file, link_for_file),'','','','', phone_number, city,  data_for_table[chat_id]['question_1'],
                            data_for_table[chat_id]['question_2'], data_for_table[chat_id]['question_3']))
    if dir == 'drawings_bank_future':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', past_link(name_file, link_for_file), '','','', phone_number, city,  '', '', data_for_table[chat_id]['job_title'], data_for_table[chat_id]['name_child'],
                            data_for_table[chat_id]['age']))
    if dir == 'video_view_bottom':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', past_link(name_file, link_for_file), '','', phone_number, city,  '', '', data_for_table[chat_id]['job_title_new'],
                             data_for_table[chat_id]['name_child_new'],'',data_for_table[chat_id]['last_name']))
    if dir == 'photo_view_from_office_window':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', '', past_link(name_file, link_for_file), '', phone_number,city))
    if dir == 'photo_before_after':
        with open('./files/data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';',  lineterminator='\n')
            writer.writerow((user_name, '', '', '', '', past_link(name_file, link_for_file), phone_number, city, '','','','','','', data_for_table[chat_id]['description']))
#//////////////////////////////////////////////////////////////