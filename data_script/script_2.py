import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread

# Конфигурация
SERVICE_ACCOUNT_FILE = 'credentials_scheduler.json'  # путь к JSON ключу
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.readonly']
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1VaeckEKf2uUfzhCf1shx0c7p9VX-Jke6TdMVGz69YDw/edit'  # ваш URL

def get_google_sheet_data():
    # Создаем credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Извлекаем ID таблицы из URL
    spreadsheet_id = SPREADSHEET_URL.split('/d/')[1].split('/')[0]
    
    # Создаем сервис для Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    
    # Получаем все листы в таблице
    spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])
    
    # Получаем данные с первого листа
    sheet_name = sheets[0]['properties']['title']  # имя первого листа
    
    # Читаем все данные с листа
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_name  # можно указать конкретный диапазон, например 'A1:Z1000'
    ).execute()
    
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return pd.DataFrame()
    
    # Преобразуем в DataFrame
    # Первая строка - заголовки
    df = pd.DataFrame(values[4:], columns=values[0])
    
    return df

# Альтернативный способ с использованием gspread (более простой)
def get_google_sheet_data_gspread():
    # Авторизация
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    
    # Открываем таблицу по URL
    spreadsheet = gc.open_by_url(SPREADSHEET_URL)
    
    # Выбираем первый лист
    worksheet = spreadsheet.get_worksheet(0)
    
    # Получаем все данные
    data = worksheet.get_all_records()
    
    # Преобразуем в DataFrame
    df = pd.DataFrame(data)
    
    return df

# Использование
if __name__ == "__main__":
    # Способ 1: Используя Google Sheets API напрямую
    df1 = get_google_sheet_data()
    print("Данные через Google Sheets API:")
    print(df1.head())
    
    # Способ 2: Используя gspread (рекомендуется)
    df2 = get_google_sheet_data_gspread()
    print("\nДанные через gspread:")
    print(df2.head())
    
    # Сохранение в CSV для дальнейшей работы
    df2.to_csv('google_sheet_data.csv', index=False)