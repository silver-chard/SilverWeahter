# coding=utf-8

import datetime
import json
import logging

from robot.IronManSuits.models.weather_data import WeatherData
from robot.weapons import db

"""
cond 
天气现象编码  中文名称             英文名称
0	        晴	                Sunny
1	        多云	                Cloudy
2	        阴	                Overcast
3	        阵雨	                Shower
4	        雷阵雨	            Thundershower
5	        雷阵雨伴有冰雹	    Thundershower with hail
6	        雨夹雪	            Sleet
7	        小雨	                Light rain
8	        中雨	                Moderate rain
9	        大雨	                Heavy rain
10	        暴雨	                Storm
11	        大暴雨	            Heavy storm
12	        特大暴雨	            Severe storm
13	        阵雪	                Snow flurry
14	        小雪	                Light snow
15	        中雪	                Moderate snow
16	        大雪	                Heavy snow
17	        暴雪	                Snowstorm
18	        雾	                Foggy
19	        冻雨	                Ice rain
20	        沙尘暴	            Duststorm
21	        小到中雨	            Light to moderate rain
22	        中到大雨	            Moderate to heavy rain
23	        大到暴雨	            Heavy rain to storm
24	        暴雨到大暴雨	        Storm to heavy storm
25	        大暴雨到特大暴雨	    Heavy to severe storm
26	        小到中雪	            Light to moderate snow
27	        中到大雪	            Moderate to heavy snow
28	        大到暴雪	            Heavy snow to snowstorm
29	        浮尘	                Dust
30	        扬沙	                Sand
31	        强沙尘暴	            Sandstorm
53	        霾	                Haze
99	        无	                Unknown
"""

"""
wind_speed
0	微风	    <5.4m/s
1	3-4级	5.5~7.9m/s
2	4-5级	8.0~10.7m/s
3	5-6级	10.8~13.8m/s
4	6-7级	13.9~17.1m/s
5	7-8级	17.2~20.7m/s
6	8-9级	20.8~24.4m/s
7	9-10级	24.5~28.4m/s
8	10-11级	28.5~32.6m/s
9	11-12级	32.7~36.9m/s
"""

"""
风向编号	中文名称	    英文名称
    0	无持续风向	 No wind
    1	东北风	     Northeast
    2	东风	         East
    3	东南风	     Southeast
    4	南风	         South
    5	西南风	     Southwest
    6	西风	         West
    7	西北风	     Northwest
    8	北风	         North
    9	旋转风	     Whirl wind

"""


def cond_str2int(cond_str):
    """
    trans weather cond string to flag(int)
    :param cond_str: string of cond in Chinese
    :return: int of cond type
    """
    try:
        return {
            '晴': 0,
            '多云': 1,
            '阴': 2,
            '阵雨': 3,
            '雷阵雨': 4,
            '雷阵雨伴有冰雹': 5,
            '雨夹雪': 6,
            '小雨': 7,
            '中雨': 8,
            '大雨': 9,
            '暴雨': 10,
            '大暴雨': 11,
            '特大暴雨': 12,
            '阵雪': 13,
            '小雪': 14,
            '中雪': 15,
            '大雪': 16,
            '暴雪': 17,
            '雾': 18,
            '冻雨': 19,
            '沙尘暴': 20,
            '小到中雨': 21,
            '中到大雨': 22,
            '大到暴雨': 23,
            '暴雨到大暴雨': 24,
            '大暴雨到特大暴雨25': 25,
            '小到中雪': 26,
            '中到大雪': 27,
            '大到暴雪': 28,
            '浮尘': 29,
            '扬沙': 30,
            '强沙尘暴': 31,
            '霾': 53,
            '无': 99
        }[cond_str]
    except KeyError as e:
        logging.warning(e)
        return -1


def cond_int2str(cond_int=0):
    """
    weather cond fag(int) trans to weather cond string 
    :param cond_int: int of cond type
    :return: string of cond
    """
    try:
        return {
            0: '晴',
            1: '多云',
            2: '阴',
            3: '阵雨',
            4: '雷阵雨',
            5: '雷阵雨伴有冰雹',
            6: '雨夹雪',
            7: '小雨',
            8: '中雨',
            9: '大雨',
            10: '暴雨',
            11: '大暴雨',
            12: '特大暴雨',
            13: '阵雪',
            14: '小雪',
            15: '中雪',
            16: '大雪',
            17: '暴雪',
            18: '雾',
            19: '冻雨',
            20: '沙尘暴',
            21: '小到中雨',
            22: '中到大雨',
            23: '大到暴雨',
            24: '暴雨到大暴雨',
            25: '大暴雨到特大暴雨25',
            26: '小到中雪',
            27: '中到大雪',
            28: '大到暴雪',
            29: '浮尘',
            30: '扬沙',
            31: '强沙尘暴',
            53: '霾',
            99: '无'
        }[cond_int]
    except KeyError as e:
        logging.warning(e)
        return "-"


def wind_speed_str2int(wind_speed_str):
    """
    trans wind speed to in flag
    :param wind_speed_str: string of wind speed : 无风 微风 .... 
    :return: 
    """
    try:
        return {
            '微风': 0,
            '3-4级': 1,
            '4-5级': 2,
            '5-6级': 3,
            '6-7级': 4,
            '7-8级': 5,
            '8-9级': 6,
            '9-10级': 7,
            '10-11级': 8,
            '11-12级': 9}[wind_speed_str]
    except KeyError as e:
        logging.warning(e)
        return "-"


def wind_speed_int2str(wind_speed_int):
    """
    trans wind speed int to string
    :param wind_speed_int: int of wind_speed
    :return: 
    """
    try:
        return {
            '微风': 0,
            '3-4级': 1,
            '4-5级': 2,
            '5-6级': 3,
            '6-7级': 4,
            '7-8级': 5,
            '8-9级': 6,
            '9-10级': 7,
            '10-11级': 8,
            '11-12级': 9}[wind_speed_int]
    except KeyError as e:
        logging.warning(e)
        return -1


def wind_dir_dtr2int(wind_dir_str):
    """
    trans wind direction string to flag(int)
    :param wind_dir_str: string of wind direction
    :return: 
    """
    try:
        return {

            '无持续风向': 0,
            '东北风': 1,
            '东风': 2,
            '东南风': 3,
            '南风': 4,
            '西南风': 5,
            '西风': 6,
            '西北风': 7,
            '北风': 8,
            '旋转风': 9,
        }[wind_dir_str]
    except KeyError as e:
        logging.warning(e)
        return -1


def wind_dir_int2str(wind_dir_int):
    """
    trans wind speed int to string
    :param wind_dir_int: 
    :return: 
    """
    try:
        return {
            0: '无持续风向',
            1: '东北风',
            2: '东风',
            3: '东南风',
            4: '南风',
            5: '西南风',
            6: '西风',
            7: '西北风',
            8: '北风',
            9: '旋转风',
        }[wind_dir_int]
    except KeyError as e:
        logging.warning(e)
        return ""


def get_date(date_str):
    try:
        day = int(date_str.split('日')[0])
    except ValueError as e:
        logging.error(e)
        return datetime.datetime.min.date()

    weather_date = datetime.datetime.now()
    while weather_date.day != day:
        weather_date += datetime.timedelta(days=1)
    return weather_date.date()


def get_time(d):
    hour_list = [2, 5, 8, 11, 14, 17, 20, 23]
    if isinstance(d, str):
        try:
            hour = int(d.split('日')[1].split('时')[0])
        except ValueError as e:
            logging.error(e)
            return -1
        if hour not in [2, 5, 8, 11, 14, 17, 20, 23]:
            logging.error('hour {} not in list'.format(hour))
            return -1
        return hour_list.index(hour)
    elif isinstance(d, int):
        if d > len(hour_list):
            logging.error('hour flag {} out of range of hour list'.format(d))
            return -1
        return hour_list[d]


def get_temp(temp):
    try:
        return float(temp.replace('℃', ''))
    except ValueError as e:
        logging.error(e)
        return 0


def is_hot(conf, redis_k):
    city_id = redis_k.split('_')[0]
    date = redis_k.split('_')[1]
    hour = redis_k.split('_')[2]

    db.get_redis_conn(conf=conf, db=conf.get('misc', 'weather_data')).smembers()


def get_weather_data(conf, city_id, weather_date, weather_time):
    if isinstance(weather_date, str):
        weather_date = datetime.datetime.strptime(weather_date, "%Y-%M-%D").date()
    if isinstance(weather_time, str):
        weather_time = ['2', '5', '8', '11', '14', '17', '20', '23'].index(weather_time)
    redis_k = '{city_id}_{date}_{hour}'.format(
        city_id=city_id,
        date=weather_date,
        hour=weather_time)
    redis = db.get_redis_conn(conf=conf, db=conf.get('misc', 'weather_data'))
    v = redis.get(redis_k)
    if not v:

        results = db.get_db_Session(conf).query(WeatherData).filter(
            WeatherData.city_id == city_id,
            WeatherData.weather_date == weather_date,
            WeatherData.weather_time == weather_time).all()
        if len(results) == 0:
            return None
        if len(results) != 1:
            logging.error([result.id for result in results])
        return {
            'city_id': city_id,
            'weather_date': results[0].weather_date,
            'weather_time': results[0].weather_time,
            'cond': results[0].cond,
            'temp': results[0].temp,
            'wind_dir': results[0].wind_dir,
            'wind_speed': results[0].wind_speed}

    v = json.loads(v)
    v['city_id'] = city_id
    v['weather_date'] = weather_date
    v['weather_time'] = weather_time
    return v
