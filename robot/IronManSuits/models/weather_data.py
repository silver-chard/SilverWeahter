# coding=utf-8
from sqlalchemy import Column, DATE, VARCHAR, INTEGER, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WeatherData(Base):
    # 表的名字:
    __tablename__ = 'weather_data'

    # 表的结构:
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    city_id = Column(VARCHAR(9), unique=True)  # 城市id
    weather_date = Column(DATE)  # 日期
    weather_time = Column(INTEGER)  # 02 05 08 11 14 17 20 23
    cond = Column(INTEGER)  # 气象状态
    temp = Column(FLOAT)  # 温度
    wind_dir = Column(INTEGER)  # 风向  0:北风, 1:东北风, 2:东风, 3:东南风, 4:南风, 5:西南风, 6:西风, 7:西北风
    wind_speed = Column(INTEGER)  # 无风 微风
