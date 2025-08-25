from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)  # BigInteger для больших ID Telegram
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(100), nullable=True)
    is_premium = Column(Boolean,)
    registration_date = Column(DateTime, default=datetime.now)

    activities = relationship("Activity", back_populates="user")

    def __str__(self):
        return f'Пользователь {self.username}, id={self.id}, tg_id={self.telegram_id}'

    def __repr__(self):
        return f'Пользователь {self.username}, id={self.id}, tg_id={self.telegram_id}'


class Activity_Type(Base):
    '''Вид активности: Основное обучение,
    Проект, Специализация, Диплом, Доп. занятия'''

    __tablename__ = "activity_types"

    id = Column(Integer, primary_key=True)
    activity_type_name = Column(String(50), unique=True)

    activity_subtypes = relationship("Activity_Subtype", back_populates="activity_type")

    def __str__(self):
        return f'{self.id}: вид активности - {self.activity_type_name}'

    def __repr__(self):
        return f'{self.id}: вид активности - {self.activity_type_name}'


class Activity_Subtype(Base):
    '''Тип активности'''

    __tablename__ = "activity_subtypes"

    id = Column(Integer, primary_key=True)
    activity_subtype_name = Column(String(50), unique=True)
    norm_time = Column(Integer, default=40, nullable=True)

    activity_type_id = Column(Integer, ForeignKey('activity_types.id'))
    activity_type = relationship("Activity_Type", back_populates="activity_subtypes")

    activities = relationship("Activity", back_populates="activity_subtype")

    def __str__(self):
        return f'{self.id}: тип активности - {self.activity_subtype_name}'

    def __repr__(self):
        return f'{self.id}: тип активности - {self.activity_subtype_name}'


class Activity(Base):
    '''Активность во время учебы'''

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_date = Column(Date)
    duration = Column(Integer, default=60)
    daypart = Column(String(50))

    user = relationship("User", back_populates="activities")

    activity_subtype_id = Column(Integer, ForeignKey('activity_subtypes.id'))
    activity_subtype = relationship("Activity_Subtype", back_populates="activity_subtype")

    created_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return f'Активность пользователя {self.user.username} номер {self.id} в {self.activity_date}'

    def __repr__(self):
        return f'Активность пользователя {self.user.username} номер {self.id} в {self.activity_date}'
