# coding=utf-8
import datetime
import logging
import math

import scipy
from numpy.core import umath
from scipy import special

from robot.weapons import data_miscs
from robot.weapons.data_miscs import cond_int2str


def get_hour_right(weather_date, weather_time):
    """
    根据日期和时间计算权制
    :param weather_time: 日期的time flag
    :param weather_date: 日期的date对象
    :return: 返回加权
    """
    hour = 0
    try:
        today_hour = 24 - datetime.datetime.now().hour  # today's hour
        days_hour = (weather_date - (
            datetime.datetime.now().date() + datetime.timedelta(days=1))).days * 24  # so far days' hour
        try:
            weather_time = data_miscs.get_time(int(weather_time))
        except ValueError as e:
            logging.error(e)
            weather_time = 0
        hour = today_hour + days_hour + weather_time
        if hour <= 0:
            return 0
        right = math.log(hour, umath.e) * -0.67 + 4.0048
        return right

    except BaseException as error_info:
        logging.error('日期加权部分(get_day_right)出错 {} {}'.format(hour, error_info))


def temp_score_gen(new_temp, old_temp):
    """
    针对温度的变化 来确定分值
    :param new_temp: 新的温度
    :param old_temp:  旧的温度
    :return:
    """
    try:
        sub_temp = new_temp - old_temp
        if not sub_temp:
            return 0
        # 标准分值
        std_score_o = 0.0875 * sub_temp ** 2
        # 标准分值(with负数)
        std_score = 0.0875 * sub_temp ** 3 / umath.sqrt(sub_temp ** 2)
        # 标准偏差值
        std_sub = scipy.special.erf(0.044721 * (new_temp - 25)) - 0.050463 * (new_temp - 25) * umath.exp(
            -0.002 * (new_temp - 25) ** 2)
        # 标准偏差值 * 系数 = 偏差值公式
        sub_score = std_score * std_sub
        # 分数等于 偏差值+标准分值
        score = std_score_o + sub_score
        return score

    except BaseException as e:
        logging.error('温度计算分值函数(temp_score_gen)出错 {}'.format(e))
        return 0


def cond_score_gen(new_cond, old_cond):
    new_cond = cond_int2str(new_cond)
    old_cond = cond_int2str(old_cond)
    if new_cond == -1 or old_cond == -1:
        return None
    new_cond = Cond(new_cond)
    old_cond = Cond(old_cond)
    if new_cond.main_class == old_cond.main_class == 'water':
        # 降水天气的分析
        score = abs(new_cond.rain_level - old_cond.rain_level) + abs(new_cond.rain_cold - old_cond.rain_cold)
    elif new_cond.main_class == 'water' or old_cond.main_class == 'water':
        # 降水天气与普通天气的分析
        score = abs(new_cond.rain_level - old_cond.rain_level)
        if new_cond.main_class == 'cloud' or old_cond.main_class == 'cloud':
            if new_cond.main_class == 'cloud':
                score += 3 - new_cond.cond_level
            else:
                score += 3 - old_cond.cond_level
        else:
            if new_cond.main_class != 'water':
                score += new_cond.cond_level
            else:
                score += old_cond.cond_level
    else:
        # 非降水天气的对比分析
        if new_cond.sub_class == old_cond.sub_class:
            score = abs(new_cond.cond_level - old_cond.cond_level)
        else:
            score = new_cond.cond_level + old_cond.cond_level - 1
    return score


class Cond:
    dict_main = {
        "晴": 'sun', "雾": 'sun', "霾": 'sun', "多云": "cloud", "阴": "cloud",
        "阵雨": "water", "雨夹雪": "water", "冻雨": "water", "小雨": "water",
        "小到中雨": "water", "中雨": "water", "中到大雨": "water", "大雨": "water",
        "大到暴雨": "water", "暴雨": "water", "暴雨到大暴雨": "water", "大暴雨": "water",
        "大暴雨到特大暴雨": "water", "特大暴雨": "water", "雷阵雨": "water",
        "雷阵雨伴有冰雹": "water", "阵雪": "water", "小雪": "water", "小到中雪": "water",
        "中雪": "water", "中到大雪": "water", "大雪": "water", "大到暴雪": "water",
        "暴雪": "water", "浮尘": 'sun', "扬沙": 'sun', "沙尘暴": 'sun', "强沙尘暴": 'sun'}

    dict_sub = {"晴": 'root', "雾": 'fog', "霾": 'fog', "多云": 'cloud', "阴": 'cloud',
                "阵雨": 'rain', "雨夹雪": 'ice', "冻雨": 'ice', "小雨": 'rain',
                "小到中雨": 'rain', "中雨": 'rain', "中到大雨": 'rain', "大雨": 'rain',
                "大到暴雨": 'rain', "暴雨": 'rain', "暴雨到大暴雨": 'rain', "大暴雨": 'rain',
                "大暴雨到特大暴雨": 'rain', "特大暴雨": 'rain', "雷阵雨": 'thunder',
                "雷阵雨伴有冰雹": 'thunder', "阵雪": 'snow', "小雪": 'snow', "小到中雪": 'snow',
                "中雪": 'snow', "中到大雪": 'snow', "大雪": 'snow', "大到暴雪": 'snow',
                "暴雪": 'snow', "浮尘": "dust", "扬沙": "dust", "沙尘暴": "dust", "强沙尘暴": "dust"}

    cond_rain_level = {"晴": 0, "雾": 0, "霾": 0, "多云": 0, "阴": 0,
                       "阵雨": 1, "雨夹雪": 2, "冻雨": 2, "小雨": 2,
                       "小到中雨": 2.5, "中雨": 3, "中到大雨": 3.5, "大雨": 4,
                       "大到暴雨": 4.5, "暴雨": 5, "暴雨到大暴雨": 5.5, "大暴雨": 6,
                       "大暴雨到特大暴雨": 6.5, "特大暴雨": 7, "雷阵雨": 1,
                       "雷阵雨伴有冰雹": 1, "阵雪": 1, "小雪": 2, "小到中雪": 2.5,
                       "中雪": 3, "中到大雪": 3.5, "大雪": 4, "大到暴雪": 4.5,
                       "暴雪": 5, "浮尘": 0, "扬沙": 0, "沙尘暴": 0, "强沙尘暴": 0}

    cond_sub_level = {"晴": 0, "雾": 1, "霾": 2, "多云": 1, "阴": 2,
                      "阵雨": 3, "雨夹雪": 4, "冻雨": 4, "小雨": 4,
                      "小到中雨": 4.5, "中雨": 5, "中到大雨": 5.5, "大雨": 6,
                      "大到暴雨": 6.5, "暴雨": 7, "暴雨到大暴雨": 7.5, "大暴雨": 8,
                      "大暴雨到特大暴雨": 8.5, "特大暴雨": 9, "雷阵雨": 3,
                      "雷阵雨伴有冰雹": 4, "阵雪": 3, "小雪": 4, "小到中雪": 4.5,
                      "中雪": 5, "中到大雪": 5.5, "大雪": 6, "大到暴雪": 6.5,
                      "暴雪": 7, "浮尘": 1, "扬沙": 2, "沙尘暴": 3, "强沙尘暴": 4}

    rain_cold_level = {"晴": 0, "雾": 0, "霾": 0, "多云": 0, "阴": 0,
                       "阵雨": 0, "雨夹雪": 2, "冻雨": 1, "小雨": 0,
                       "小到中雨": 0, "中雨": 0, "中到大雨": 0, "大雨": 0,
                       "大到暴雨": 0, "暴雨": 0, "暴雨到大暴雨": 0, "大暴雨": 0,
                       "大暴雨到特大暴雨": 0, "特大暴雨": 0, "雷阵雨": 0,
                       "雷阵雨伴有冰雹": 1, "阵雪": 3, "小雪": 3, "小到中雪": 3,
                       "中雪": 3, "中到大雪": 3, "大雪": 3, "大到暴雪": 3,
                       "暴雪": 3, "浮尘": 0, "扬沙": 0, "沙尘暴": 0, "强沙尘暴": 0}

    def __init__(self, cond_str):
        self.cond_str = cond_str
        self.main_class = self.dict_main[cond_str]
        self.sub_class = self.dict_sub[cond_str]

        self.rain_cold = self.rain_cold_level[cond_str]
        self.rain_level = self.cond_rain_level[cond_str]
        self.cond_level = self.cond_sub_level[cond_str]


def wind_speed_gen(new_wind_s, old_wind_s):
    return abs(new_wind_s - old_wind_s)


def wind_dir_gen(new_wind_d, old_wind_d):
    if not (isinstance(new_wind_d, int) and isinstance(old_wind_d, int)):
        return 0
    if new_wind_d in [0, 9] or old_wind_d in [0, 9]:
        return 1
    sub = abs(new_wind_d - old_wind_d)
    if sub < 5:
        return sub
    return 4 - sub % 4
