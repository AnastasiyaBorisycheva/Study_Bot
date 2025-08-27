import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from pprint import pprint

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

load_dotenv()

info = {
    'type':  os.environ['TYPE'],
    'project_id':  os.environ['PROJECT_ID'],
    'private_key_id':  os.environ['PRIVATE_KEY_ID'],
    'private_key':  os.environ['PRIVATE_KEY'],
    'client_email':  os.environ['CLIENT_EMAIL'],
    'client_id':  os.environ['CLIENT_ID'],
    'auth_uri':  os.environ['AUTH_URI'],
    'token_uri':  os.environ['TOKEN_URI'],
    'auth_provider_x509_cert_url':  os.environ['AUTH_PROVIDER_X509_CERT_URL'],
    'client_x509_cert_url':  os.environ['CLIENT_X509_CERT_URL']
}

# Функция авторизации.
def auth():
    credentials = Credentials.from_service_account_info(
        info=info, scopes=SCOPES)
    service = discovery.build('drive', 'v3', credentials=credentials)
    return service

# Функция получения списка файлов на диске
def get_list_obj(service):
    response = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'")
    return response.execute()

service = auth()
pprint(get_list_obj(service)) 


get_list=get_list_obj(service)

for key_1 in get_list:
    print(key_1)
    if key_1 =='files':
        print(get_list[key_1][0])
        # for key, value in value_1[0]:
        #     if key=='id':
        #         print(value)
            

# Удаление файлов с диска сервисного аккаунта
def clear_disk(service, spreadsheets):
    for spreadsheet in spreadsheets:
        response = service.files().delete(fileId=spreadsheet['id'])
        response.execute()
service = auth()
spreadsheets = get_list_obj(service)['files']
# pprint(spreadsheets)
# clear_disk(service, spreadsheets) 