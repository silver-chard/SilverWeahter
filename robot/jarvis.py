# coding=utf-8
import ConfigParser
import json
import time
import urllib2

from robot.IronManSuits.suits import MarkI
from robot.weapens import db


class Jarvis:
    """
    Jarvis 可以制作和管理许多suit 
    每个suit可以获取天气信息 分析 等等……
    """
    def __init__(self, config_path='config.ini'):

        conf = ConfigParser.ConfigParser()
        conf.read(config_path)
        if not conf.sections():
            exit(1)
        self.conf = conf
        self.db = db.get_db_conn(conf=conf)
        self.city_list_redis = db.get_redis_conn(conf=conf, db=self.conf.get('misc', 'city_list_redis'))
        if self.conf.get('misc', 'debug'):
            self.city_list_redis.flushall()
        self.weather_data_redis = db.get_redis_conn(conf=conf, db=self.conf.get('misc', 'weather_data'))

    def search_provinces(self):
        prov_req = urllib2.Request('http://www.weather.com.cn/data/city3jdata/china.html')
        prov_req.add_header('Referer', 'http://www.weather.com.cn/pubmodel/inquires2.htm')
        data = urllib2.urlopen(prov_req)
        provs = json.loads(data.read())
        for prov_no in provs:
            self.city_list_redis.set(
                'china_{prov_no}'.format(prov_no=prov_no), provs[prov_no],
                ex=self.conf.get('misc', 'city_list_expires'))
        # print {prov_id: self.city_list_redis.get(prov_id) for prov_id in self.city_list_redis.keys('prov_*')}
        for prov_no in provs:
            self.search_cities(prov_no)

    def search_cities(self, prov_no):
        """
        search_cities 结构最为复杂 因为涉及到直辖市 和 普通的省市结构
        对于省市结构的模型 直接根据省查找市 根据市查找区 flag = 0 city_101PPCC (特征是city_7位)
        对于直辖市结构模型 直接根据省查找站 把站id存入 flag = 1 city_101PPSS00 (特征是city_9位)
        
        :param prov_no: 
        :return: 
        """
        city_req = urllib2.Request(
            'http://www.weather.com.cn/data/city3jdata/provshi/{prov_no}.html'.format(prov_no=prov_no))
        city_req.add_header('Referer', 'http://www.weather.com.cn/pubmodel/inquires2.htm')
        data = urllib2.urlopen(city_req)
        cities = json.loads(data.read())

        for city_no in cities:
            if len(cities) == 1:
                # for city in cities:
                self.search_stations(prov_no, city_no, flag=1)
            else:
                self.city_list_redis.set(
                    'city_{prov_no}_{city_no}'.format(prov_no=prov_no, city_no=city_no),
                    cities[city_no],
                    self.conf.get('misc', 'city_list_expires')
                )
                self.search_stations(prov_no, city_no, flag=0)

    def search_stations(self, prov_no, city_no, flag=0):

        station_req = urllib2.Request(
            'http://www.weather.com.cn/data/city3jdata/station/{0}{1}.html'.format(prov_no, city_no))
        station_req.add_header('Referer', 'http://www.weather.com.cn/pubmodel/inquires2.htm')
        data = urllib2.urlopen(station_req)
        stations = json.loads(data.read())
        if flag == 0:
            for station_no in stations:
                if len(station_no) == 2:
                    self.city_list_redis.set(
                        'station_{prov_no}_{city_no}_{prov_no}{city_no}{station_no}'.format(
                            prov_no=prov_no, city_no=city_no, station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )
                    self.city_list_redis.set(
                        'list_{prov_no}{city_no}{station_no}'.format(
                            prov_no=prov_no, city_no=city_no, station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )

                else:
                    self.city_list_redis.set(
                        'station_{prov_no}_{city_no}_{station_no}'.format(
                            prov_no=prov_no, city_no=city_no, station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )
                    self.city_list_redis.set(
                        'list_{station_no}'.format(station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )
        elif flag == 1:
            for station_no in stations:
                if len(station_no) == 2:
                    self.city_list_redis.set(
                        'city_{prov_no}_{prov_no}{station_no}{city_no}'.format(
                            prov_no=prov_no, city_no=city_no, station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires'))
                    self.city_list_redis.set(
                        'list_{prov_no}{station_no}{city_no}'.format(
                            prov_no=prov_no, city_no=city_no, station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )
                else:
                    self.city_list_redis.set(
                        'city_{prov_no}_{station_no}'.format(prov_no=prov_no, station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )
                    self.city_list_redis.set(
                        'list_{station_no}'.format(station_no=station_no),
                        stations[station_no],
                        self.conf.get('misc', 'city_list_expires')
                    )

    def suit_maker(self):
        # todo: 根据city_id 准备一群suits 然后运行每个suit
        city_ids = self.city_list_redis.get('list_*')
        print "已有城市:", len(city_ids)
        for city_id in city_ids:
            city = MarkI(city_id=city_id, conf=self.conf)
            print city.get_data()

    def target(self):
        # todo: 每日凌晨执行，同步weather.com.cn线上城市结构
        pass

if __name__ == '__main__':
    j = Jarvis('config.ini')
    start = time.time()
    j.search_provinces()
    print time.time() - start, 's'
    j.suit_maker()
