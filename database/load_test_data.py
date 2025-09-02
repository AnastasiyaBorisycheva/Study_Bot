import csv
import os
import argparse
from datetime import datetime, date
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Импортируем модели напрямую (предполагаем, что файл в той же директории)
from models import Base, User, Activity_Type, Activity_Subtype, Activity


class TestDataLoader:
    def __init__(self, db_url='sqlite:///study_test.db'):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.db_url = db_url
        
    def check_tables_exist(self):
        """Проверяет, существуют ли таблицы в базе"""
        inspector = inspect(self.engine)
        required_tables = ['users', 'activity_types', 'activity_subtypes', 'activities']
        existing_tables = inspector.get_table_names()
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            print(f"Внимание: Отсутствуют таблицы: {missing_tables}")
            print("Создаем таблицы...")
            Base.metadata.create_all(self.engine)
            print("Таблицы созданы успешно!")
        
    def load_users_from_csv(self, csv_file_path):
        """Загрузка пользователей из CSV"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                users = []
                
                for row in reader:
                    user = User(
                        telegram_id=int(row['telegram_id']),
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        username=row['username'],
                        is_premium=row['is_premium'].lower() == 'true',
                        registration_date=datetime.strptime(row['registration_date'], '%Y-%m-%d %H:%M:%S') if row['registration_date'] else datetime.now()
                    )
                    users.append(user)
                
                session = self.Session()
                session.add_all(users)
                session.commit()
                print(f"✓ Загружено {len(users)} пользователей")
                session.close()
                
        except Exception as e:
            print(f"✗ Ошибка при загрузке пользователей: {e}")
            raise

    def load_activity_types_from_csv(self, csv_file_path):
        """Загрузка типов активности из CSV"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                activity_types = []
                
                for row in reader:
                    activity_type = Activity_Type(
                        activity_type_name=row['activity_type_name']
                    )
                    activity_types.append(activity_type)
                
                session = self.Session()
                session.add_all(activity_types)
                session.commit()
                print(f"✓ Загружено {len(activity_types)} типов активности")
                session.close()
                
        except Exception as e:
            print(f"✗ Ошибка при загрузке типов активности: {e}")
            raise

    def load_activity_subtypes_from_csv(self, csv_file_path):
        """Загрузка подтипов активности из CSV"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                activity_subtypes = []
                
                for row in reader:
                    activity_subtype = Activity_Subtype(
                        activity_subtype_name=row['activity_subtype_name'],
                        norm_time=int(row['norm_time']) if row['norm_time'] else 40,
                        activity_type_id=int(row['activity_type_id'])
                    )
                    activity_subtypes.append(activity_subtype)
                
                session = self.Session()
                session.add_all(activity_subtypes)
                session.commit()
                print(f"✓ Загружено {len(activity_subtypes)} подтипов активности")
                session.close()
                
        except Exception as e:
            print(f"✗ Ошибка при загрузке подтипов активности: {e}")
            raise

    def load_activities_from_csv(self, csv_file_path):
        """Загрузка активностей из CSV"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                activities = []
                
                for row in reader:
                    activity = Activity(
                        telegram_id=int(row['telegram_id']),
                        activity_date=datetime.strptime(row['activity_date'], '%Y-%m-%d').date(),
                        duration=int(row['duration']),
                        daypart=row['daypart'],
                        activity_subtype_id=int(row['activity_subtype_id'])
                    )
                    activities.append(activity)
                
                session = self.Session()
                session.add_all(activities)
                session.commit()
                print(f"✓ Загружено {len(activities)} активностей")
                session.close()
                
        except Exception as e:
            print(f"✗ Ошибка при загрузке активностей: {e}")
            raise

    def create_test_data(self, data_dir='database/test_data'):
        """Основная функция загрузки данных"""
        
        print(f"Загрузка тестовых данных из {data_dir}...")
        print(f"База данных: {self.db_url}")
        print("-" * 50)
        
        try:
            # Проверяем и создаем таблицы если нужно
            self.check_tables_exist()
            
            # Создаем директорию для тестовых данных, если её нет
            os.makedirs(data_dir, exist_ok=True)
            
            # Пути к CSV файлам
            users_csv = os.path.join(data_dir, 'users.csv')
            activity_types_csv = os.path.join(data_dir, 'activity_types.csv')
            activity_subtypes_csv = os.path.join(data_dir, 'activity_subtypes.csv')
            activities_csv = os.path.join(data_dir, 'activities.csv')
            
            # Загрузка в правильном порядке (важен порядок из-за foreign keys)
            if os.path.exists(users_csv):
                self.load_users_from_csv(users_csv)
            else:
                print(f"✗ Файл {users_csv} не найден")
            
            if os.path.exists(activity_types_csv):
                self.load_activity_types_from_csv(activity_types_csv)
            else:
                print(f"✗ Файл {activity_types_csv} не найден")
            
            if os.path.exists(activity_subtypes_csv):
                self.load_activity_subtypes_from_csv(activity_subtypes_csv)
            else:
                print(f"✗ Файл {activity_subtypes_csv} не найден")
            
            if os.path.exists(activities_csv):
                self.load_activities_from_csv(activities_csv)
            else:
                print(f"✗ Файл {activities_csv} не найден")
            
            print("-" * 50)
            print("✅ Загрузка данных завершена!")
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")

    def generate_sample_csv_files(self, data_dir='/database/test_data'):
        """Генерация примеров CSV файлов"""
        
        print(f"Создание примеров CSV файлов в {data_dir}...")
        
        os.makedirs(data_dir, exist_ok=True)
        
        # Пример users.csv
        users_data = [
            ['telegram_id', 'first_name', 'last_name', 'username', 'is_premium', 'registration_date'],
            ['123456789', 'Иван', 'Иванов', 'ivanov', 'True', '2024-01-15 10:30:00'],
            ['987654321', 'Мария', 'Петрова', 'maria_p', 'False', '2024-01-16 14:20:00'],
            ['555555555', 'Алексей', 'Сидоров', 'alex_s', 'True', '2024-01-17 09:15:00']
        ]
        
        with open(os.path.join(data_dir, 'users.csv'), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(users_data)
        print(f"✓ Создан users.csv")
        
        # Пример activity_types.csv
        activity_types_data = [
            ['activity_type_name'],
            ['Основное обучение'],
            ['Проект'],
            ['Специализация'],
            ['Диплом'],
            ['Доп. занятия']
        ]
        
        with open(os.path.join(data_dir, 'activity_types.csv'), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(activity_types_data)
        print(f"✓ Создан activity_types.csv")
        
        # Пример activity_subtypes.csv
        activity_subtypes_data = [
            ['activity_subtype_name', 'norm_time', 'activity_type_id'],
            ['Лекции', '40', '1'],
            ['Практика', '45', '1'],
            ['Проектная работа', '60', '2'],
            ['Исследование', '50', '3'],
            ['Написание диплома', '120', '4'],
            ['Дополнительные курсы', '30', '5']
        ]
        
        with open(os.path.join(data_dir, 'activity_subtypes.csv'), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(activity_subtypes_data)
        print(f"✓ Создан activity_subtypes.csv")
        
        # Пример activities.csv
        activities_data = [
            ['telegram_id', 'activity_date', 'duration', 'daypart', 'activity_subtype_id'],
            ['123456789', '2024-01-20', '120', 'утро', '1'],
            ['123456789', '2024-01-20', '90', 'вечер', '2'],
            ['987654321', '2024-01-21', '180', 'день', '3'],
            ['555555555', '2024-01-22', '60', 'утро', '4'],
            ['987654321', '2024-01-23', '240', 'день', '5']
        ]
        
        with open(os.path.join(data_dir, 'activities.csv'), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(activities_data)
        print(f"✓ Создан activities.csv")
        
        print(f"✅ Примеры CSV файлов созданы в папке {data_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Загрузка тестовых данных в базу данных',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python load_test_data.py --db sqlite:///my_database.db
  python load_test_data.py --generate --data-dir my_data
  python load_test_data.py --db sqlite:///test.db --data-dir csv_data
'''
    )
    
    parser.add_argument('--db', default='sqlite:///study_test.db', 
                       help='URL базы данных (по умолчанию: sqlite:///study_test.db)')
    parser.add_argument('--data-dir', default='database/test_data', 
                       help='Директория с CSV файлами (по умолчанию: test_data)')
    parser.add_argument('--generate', action='store_true',
                       help='Сгенерировать примеры CSV файлов')

    args = parser.parse_args()
    
    loader = TestDataLoader(args.db)
    
    if args.generate:
        loader.generate_sample_csv_files(args.data_dir)
    else:
        loader.create_test_data(args.data_dir)

if __name__ == "__main__":
    main()