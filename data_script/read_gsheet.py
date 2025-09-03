import gspread
import os
import pandas as pd
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

# Конфигурация
SERVICE_ACCOUNT_FILE = 'credentials_scheduler.json'  # путь к JSON ключу
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.readonly']
SPREADSHEET_URL = os.getenv('SPREADSHEET_URL')   # ваш URL


def get_google_sheet_data():
    # Создаем credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Извлекаем ID таблицы из URL
    spreadsheet_id = SPREADSHEET_URL.split('/d/')[1].split('/')[0]


def get_specific_range(file_name='new_csv.csv'):
    """Получение конкретного диапазона данных"""
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.worksheet("List")
    
    # Получить конкретный диапазон
    range_data = worksheet.get('A1:H500')  # ячейки A1:G500
    df = pd.DataFrame(range_data[0:], columns=range_data[0])
    # print(df)
    return df.to_csv('data_script/'+file_name+'.csv', index=False, encoding='utf-8')


get_specific_range('unpreparing_stady_data')