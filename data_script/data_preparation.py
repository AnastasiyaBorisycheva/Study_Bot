import os

import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from matplotlib import pyplot as pl
from read_gsheet import get_specific_range, get_activity_subtypes, get_activity_types

# Выгрузим исходные данные из Google таблицы
get_specific_range('unpreparing_stady_data')

# Подготовим таблицу 'activity_subtype' для загрузки в базу данных
get_activity_subtypes()

# Подготовим таблицу 'activity_type' для загрузки в базу данных
get_activity_types()

# Создадим датафрейм и положим его в переменную df
df = pd.read_csv('data_script/unpreparing_stady_data.csv',header=1, date_format=True, dayfirst=True).drop_duplicates()

# Приведем все данные по активностям к единому виду
df = df.rename(columns={'Вид активности':'rank',
                   'Спринт':'activity_subtype_name',
                    'Дата':'activity_date',
                    'Утро':'morning',
                    'Вечер':'evening',
                    'Доп занятия':'add_study_duration',
                    'Название':'add_study_type'}).drop(columns=['Модули\Спринты','rank'])

# Приведем столбец activity_date к формату даты и заполним пропуски в датафремеме на 0
df.activity_date = pd.to_datetime(df['activity_date'], format='%d.%m.%Y')
df.activity_date = df.activity_date.dt.date
df = df.fillna(0)

# Перевод данных из полей morning, evening и add_study в отдельные строки. Приведение датафрейма к формату duration - daypart  
# Выделим только утренне активности в отдельный датафрейм
morning_df = df.query('morning != 0 & activity_date !=0')\
    .drop(columns=['add_study_duration','add_study_type','evening'])
morning_df['daypart'] = 'Утро'
morning_df['morning'] = morning_df['morning'].astype(int)
morning_df = morning_df.rename(columns={'morning':'duration'})

# Выделим только вечерние активности в отдельный датафрейм
evening_df = df.query('evening != 0 & activity_date !=0')\
    .drop(columns=['add_study_duration','add_study_type','morning'])
evening_df['daypart'] = 'Вечер'
evening_df['evening'] = evening_df['evening'].astype(int)
evening_df = evening_df.rename(columns={'evening':'duration'})

# Выделим только вебинары в отдельный датафрейм
web_df = df.query('add_study_type == "Вебинар"')
web_df = web_df.drop(columns='activity_subtype_name')\
     .rename(columns={'add_study_type':'activity_subtype_name'})
web_df['duration'] = web_df['add_study_duration']
web_df['daypart'] = 'Вечер'
web_df = web_df.drop(columns=['morning','evening','add_study_duration'])
web_df['duration'] = web_df['duration'].astype(int)

# Выделим только дополнительные активности в отдельный датафрейм
add_study_df = df.query('add_study_type != 0 & activity_date !=0 & add_study_type != "Вебинар"')
add_study_df = add_study_df.drop(columns='activity_subtype_name')\
    .rename(columns={'add_study_type':'activity_subtype_name','duration':'add_study_duration'})

# Разделим дополнительные активности на утренние и дневные в ручном режиме
add_study_df['duration_evening'] = add_study_df.add_study_duration
add_study_df['duration_morning'] = 0
add_study_df.loc[38,'duration_evening'] =120
add_study_df.loc[39,'duration_evening'] = 20
add_study_df.loc[52,'duration_evening'] = 30
add_study_df.loc[52,'duration_morning'] = 120
add_study_df.loc[63,'duration_evening'] = 60
add_study_df.loc[63,'duration_morning'] = 120
add_study_df.loc[64,'duration_morning'] = 120
add_study_df.loc[64,'duration_evening'] = 120
add_study_df.loc[66,'duration_morning'] = 120
add_study_df.loc[66,'duration_evening'] = 60
add_study_df.loc[67,'duration_morning'] = 120
add_study_df.loc[67,'duration_evening'] = 120
add_study_df.loc[74,'duration_morning'] = 120
add_study_df.loc[74,'duration_evening'] = 120
add_study_df.loc[76,'duration_morning'] = 120
add_study_df.loc[76,'duration_evening'] = 60
add_study_df.loc[77,'duration_morning'] = 120
add_study_df.loc[77,'duration_evening'] = 120
add_study_df.loc[78,'duration_morning'] = 120
add_study_df.loc[78,'duration_evening'] = 240
add_study_df.loc[79,'duration_morning'] = 120
add_study_df.loc[79,'duration_evening'] = 120
add_study_df.loc[86,'duration_morning'] = 60
add_study_df.loc[86,'duration_evening'] = 60

# Выделим только утренние дополнительные активности в отдельный датафрейм
add_study_morning = add_study_df.query('duration_morning != 0')\
    .drop(columns=['morning','evening','add_study_duration','duration_evening'])\
    .rename(columns={'duration_morning':'duration'})
add_study_morning.duration = pd.to_numeric(add_study_morning.duration)
add_study_morning['daypart'] = 'Утро'

# Выделим только вечерние дополнительные активности в отдельный датафрейм
add_study_evening = add_study_df.query('duration_evening != 0')\
    .drop(columns=['morning','evening','add_study_duration','duration_morning'])\
    .rename(columns={'duration_evening':'duration'})
add_study_evening['duration'] = add_study_evening['duration'].astype(int)
add_study_evening['daypart'] = 'Вечер'

# Объединяем все очищенные датафреймы в один и сохраняем в .csv
clear_df = pd.concat([morning_df,evening_df,add_study_evening,add_study_morning,web_df])

# Выгрузим данные таблицы activities_subtypes в датафрейм и опредилим activities_subtypes_id с помощью индекса
activities_subtypes_df = pd.read_csv('data_script/activity_subtypes.csv').reset_index()
activities_subtypes_df['activity_subtype_id'] = activities_subtypes_df.index+1

# Подготовим таблицу 'activities' для загрузки в базу данных
# Выгрузим телеграм id из .env-файла
load_dotenv()
telegram_id=os.getenv('TG_ID')

# Выгрузим объединим подготовленный датафрейм с активностями с датафреймом activities_subtypes_df
# Добавим столбец с телеграм id и удалим лишние столбцы
activities=pd.merge(clear_df,activities_subtypes_df, how='left', on='activity_subtype_name')\
    .drop(columns=['activity_subtype_name','norm_time','activity_type_id','index','norm_time'])
activities['telegram_id']=telegram_id

# Сохраним готовую таблицу в .csv файл
activities.to_csv('data_script/activities.csv', index=False)

# Выведем проверочную строку в консоль
check_df = pd.read_csv('data_script/activities.csv')
check_df = check_df.sort_values('activity_date',ascending=False).head(1)
print(check_df)