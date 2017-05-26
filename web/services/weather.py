# coding=utf-8
import datetime
import json
import logging

from models.weather_data import WeatherData
from services.tools import get_redis, get_conf, get_session


def bin_2_time(weather_flag):
    weather_flag = int(weather_flag)
    time_list = [2, 5, 8, 11, 14, 17, 20, 23][::-1]
    time_result = []
    while weather_flag > 0:
        if weather_flag % 2:
            time_result.append(time_list.pop())
        else:
            time_list.pop()
        weather_flag /= 2
    return time_result


def int_2_time(weather_flag):
    time_list = [2, 5, 8, 11, 14, 17, 20, 23]
    try:
        return time_list[weather_flag]
    except IndexError:
        return None


def time_2_int(weather_time):
    time_list = {2: 0, 5: 1, 8: 2, 11: 3, 14: 4, 17: 5, 20: 6, 23: 7}
    try:
        return time_list[weather_time]
    except KeyError:
        return None


def str_2_date(weather_date):
    if isinstance(weather_date, str):
        return datetime.datetime.strptime(weather_date, '%Y-%m-%d').date()
    return None


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


def weather_data_format(result):
    return map(lambda a: {
        'weather_date': a['weather_date'],
        'weather_time': '{}:00'.format(int_2_time(a['weather_time'])),
        'cond': cond_int2str(a['cond']),
        'temp': a['temp'],
        'wind_dir': wind_dir_int2str(a['wind_dir']),
        'wind_speed': wind_speed_int2str(a['wind_speed'])
    }, result)


def get_data(city_id, weather_date, weather_time):
    weather_date = str_2_date(weather_date)
    weather_time = bin_2_time(weather_time)
    weather_time_flags = [time_2_int(t) for t in weather_time]

    result_redis = []
    # get data from redis
    for t in weather_time_flags:
        k = '{city_id}_{weather_date}_{weather_time}'.format(city_id=city_id, weather_date=weather_date, weather_time=t)
        conf = get_conf()
        redis = get_redis(conf=conf, db=conf.getint('redis', 'weather_date_redis'))
        v = redis.get(k)
        data = json.loads(v)
        if data:
            data['weather_time'] = t
            data['weather_date'] = weather_date
            result_redis.append(data)
            weather_time_flags.remove(t)

    if not weather_time_flags:
        return weather_data_format(result_redis)
    # get data from db
    session = get_session()
    results_db = session.query(WeatherData).filter(
        WeatherData.city_id == city_id,
        WeatherData.weather_date == weather_date,
        WeatherData.weather_time in weather_time_flags).all()
    results_db = map(lambda a: {'wind_speed': a.wind_speed, 'wind_dir': a.wind_dir, 'cond': a.cond, 'temp': a.temp,
                                'weather_time': a.weather_time, 'weather_date': a.weather_date}, results_db)
    results = results_db + result_redis
    return weather_data_format(results)
