
import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient import discovery

load_dotenv() 
MY_EMAIL = os.getenv("EMAIL")

# Константы
SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        ] 

## rename your downloaede credential file to 'TOKEN.json' and add in main directory of project
CREDENTIALS_FILE = 'credentials_scheduler.json'

# Функция авторизации
def auth():
    # Создаём экземпляр класса Credentials.
    credentials = Credentials.from_service_account_file(
                  filename=CREDENTIALS_FILE, scopes=SCOPES)
    # Создаём экземпляр класса Resource.
    service = discovery.build('sheets', 'v4', credentials=credentials)
    print('Выполнили АУФ')
    print('credentials=',credentials,'service=',service)
    return service, credentials
    

# Функция создания документа
def create_spreadsheet(service):
    # Тело spreadsheet
    spreadsheet_body = {
         # Свойства документа
        'properties': {
            'title': 'Бюджет путешествий',
            'locale': 'ru_RU'
        },
        # Свойства листов документа
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Отпуск 2079',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 100
                }
             }
         }]
    }
    request = service.spreadsheets().create(body=spreadsheet_body)
    print('request=',request)
    response = request.execute()
    print('response=',response)
    spreadsheet_id = response['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
    return spreadsheet_id 

# Вызов функций
service, credentials = auth()
spreadsheetId = create_spreadsheet(service)
print('это спредшит айди=',spreadsheetId) 

# Функция выдачи прав доступа
def set_user_permissions(spreadsheet_id, credentials):
    permissions_body={'type': 'user',                               # Тип учётных данных.
                      'role': 'writer',                             # Права доступа для учётной записи.
                      'emailAddress': 'dmitriy.borisychev.ads@gmail.com'}                     # Ваш личный гугл-аккаунт.
    
    # Создаётся экземпляр класса Resource для Google Drive API.
    drive_service = discovery.build('drive', 'v3', credentials=credentials)
    
    # Формируется и сразу выполняется запрос на выдачу прав вашему аккаунту.
    drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permissions_body,
        fields='id'
    ).execute() 

# Вызов функции
set_user_permissions()