from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from settings import id_table

SAMPLE_RANGE_NAME = 'Test List!A2:E246'


class GoogleSheet:
    SPREADSHEET_ID = id_table
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID,
                                                                  body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def add(self, range, values):

        body = {'values':[values]}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID, range=range,
            valueInputOption='USER_ENTERED', body=body).execute()


def main():
    gs = GoogleSheet()
    test_range = 'Лист1!A1'

    # gs.updateRangeValues(test_range, test_values)
    gs.add(range=test_range, values=[2,3,4,'строка'])
    gs.add(range=test_range, values=[2, 3, 4, 'строка'])


if __name__ == '__main__':
    main()