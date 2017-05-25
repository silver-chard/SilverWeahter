# coding=utf-8
from sqlalchemy import Column, DATE, VARCHAR, INTEGER, FLOAT, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WeatherData(Base):
    # 表的名字:
    __tablename__ = 'weather_data'
    __table_args__ = (
        UniqueConstraint('city_id', 'weather_date', 'weather_time', name='city_id_weather_date_weather_time'),
        Index('city_id_weather_date', 'city_id', 'weather_date'),
        Index('city_id', 'city_id')
    )

    # 表的结构:
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    city_id = Column(INTEGER, index=True)  # 城市id
    weather_date = Column(DATE, index=True)
    weather_time = Column(INTEGER, index=True)
    cond = Column(INTEGER)
    temp = Column(FLOAT)
    wind_dir = Column(INTEGER)
    wind_speed = Column(INTEGER)
    meta = Column(VARCHAR(2048))
