from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from settings import id_table

import google.auth
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def add( service_table, values, range = None):
    range = 'Лист1!A1'
    SPREADSHEET_ID = id_table
    body = {'values': [values]}
    result = service_table.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=range,
        valueInputOption='USER_ENTERED', body=body).execute()


def upload_to_folder(real_folder_id, file_for_load, file_name, user_name, phone_number, city, question_1='', question_2='', question_3='', name_age='', job_title='', description='', last_name=''):
    SCOPES = ['https://www.googleapis.com/auth/drive'+'https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('flow')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # create drive api client
        service_drive = build('drive', 'v3', credentials=creds)
        service_table = build('sheets', 'v4', credentials=creds)

        if real_folder_id == '1FfaFJrv2NZYVPwaAV3K0dtmKaWBdTMfo':
            folder_id = real_folder_id
            file_metadata = {
                'name': f'{file_name}',
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_for_load, mimetype='video/mp4', resumable=True)
            # pylint: disable=maybe-no-member
        else:
            folder_id = real_folder_id
            file_metadata = {
                'name': f'{file_name}',
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_for_load, mimetype='image/jpg', resumable=True)
            # pylint: disable=maybe-no-member

        file = service_drive.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()

        #запись в таблицу
        file_id_drive = file.get('id')
        list_for_add = []
        if real_folder_id == '1nDtWwr9PuKHK--g4VqVGmGuRQ23eQ0zD':
            list_for_add = [user_name,
                            f'=ГИПЕРССЫЛКА("https://drive.google.com/file/d/{file_id_drive}/view?usp=sharing"; "{file_name}")','','','','', phone_number, city, question_1, question_2, question_3]
        elif real_folder_id == '1j6Ry93iaxJkzY6cCNGk9Y1NxjShraEfP':
            list_for_add = [user_name, '',
                            f'=ГИПЕРССЫЛКА("https://drive.google.com/file/d/{file_id_drive}/view?usp=sharing"; "{file_name}")','','','', phone_number, city,'','','', name_age, job_title]
        elif real_folder_id == '1FfaFJrv2NZYVPwaAV3K0dtmKaWBdTMfo':
            list_for_add = [user_name, '', '',
                            f'=ГИПЕРССЫЛКА("https://drive.google.com/file/d/{file_id_drive}/view?usp=sharing"; "{file_name}")','','', phone_number, city,'','','', '', job_title, '', last_name]
        elif real_folder_id == '1LrmRdzERk4UocJFkH88GBt9fjQB04VTv':
            list_for_add = [user_name, '', '', '',
                            f'=ГИПЕРССЫЛКА("https://drive.google.com/file/d/{file_id_drive}/view?usp=sharing"; "{file_name}")','', phone_number, city]
        elif real_folder_id == '1Njz5FdvAcElVY6rFucxCX7Ffh-IL_AkT':
            list_for_add = [user_name, '', '', '', '',
                            f'=ГИПЕРССЫЛКА("https://drive.google.com/file/d/{file_id_drive}/view?usp=sharing"; "{file_name}")', phone_number, city, '', '','', '','', description]
        add(service_table=service_table, values=list_for_add)

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')

