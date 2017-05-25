# coding=utf-8
from sqlalchemy import Column, INTEGER, FLOAT, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WeatherScore(Base):
    # 表的名字:
    __tablename__ = 'weather_score'
    __table_args__ = (
        Index('city_id', 'city_id'),
    )

    # 表的结构:
    city_id = Column(INTEGER, index=True, primary_key=True)  # 城市id
    temp = Column(FLOAT, default=0)
    cond = Column(FLOAT, default=0)
    wind_speed = Column(FLOAT, default=0)
    wind_dir = Column(FLOAT, default=0)
