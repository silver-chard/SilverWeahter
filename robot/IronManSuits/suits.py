# coding=utf-8
import json
import logging
import time
import urllib
from logging import config

import bs4


class MarkI:
    def __init__(self, city_id, conf):
        self.city_id = city_id
        self.conf = conf
        self.get_data()

    def __del__(self):
        pass

    def db_conn(self):
        """
        db orm 获取
        :return: 
        """
        # 初始化数据库连接:
        # defengine = create_engine(
        #     'mysql+mysqlconnector://{user}:{pwd}@{host}:3306/{db}'.format(user=user, pwd=password, host=host, db=db))
        # 创建DBSession类型:
        # DBSession = sessionmaker(bind=engine)
        pass

    def redis(self):
        """
        redis链接获取
        :return: 
        """
        return

    def get_data(self):
        """
        获取数据的方法 会循环尝试获取数次
        :return: 
        """
        err_count = 0
        while not self.__get_data() and err_count < self.conf.get('misc', 'max_err'):
            err_count += 1
        if err_count == self.conf.get('misc', 'max_err'):
            return None
        else:
            if "7d" in self.weather_data:
                return self.weather_data["7d"]
            else:
                logging.warning("weather_data don't have '7d' :", self.weather_data)
                return

    def __get_data(self):
        req = urllib.urlopen('http://www.weather.com.cn/weather/{city_id}.shtml'.format(city_id=self.city_id))
        if req.getcode() / 100 == 2:
            weather_html = bs4.BeautifulSoup(req.read(), "html.parser")
            try:
                data = filter(lambda a: a.text.find('hour3data') > -1, weather_html.find_all('script'))[0].text
            except IndexError as e:
                logging.error(e)
                return None
            try:
                self.weather_data = json.loads(data[data.find('{'):])
                return True
            except ValueError as e:
                logging.error(e)
                return None
            except TypeError as e:
                logging.error(e)
                return None
        else:
            logging.error(req.read(), req.getcode())
            return None

    def analyze(self):
        pass

    def save_data(self):
        pass

    def save_history(self):
        pass

    def start(self):
        self.weather_data = self.get_data()


if __name__ == '__main__':
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #     datefmt='%Y-%b-%d:%H:%M:%S',
    #     filname='robot_run_error.log',
    #     filemode='a+',
    #     disable_existing_loggers=0,
    #     maxbytes=0
    #
    # )
    # conf = ConfigParser.ConfigParser()
    # conf.read("../config/config.ini")
    # r = MarkI(101010300, conf)
    # res = r.get_data()

    logging.config.fileConfig("../config/log.conf")
    logging.error(time.time())
    time.sleep(0.1)
    logging.error(time.time())
