# coding=utf-8
from handlers.basehandlers.basehandler import BaseHandler
from services.city import get_province, get_city_id, get_station_id


class GetProvince(BaseHandler):
    def post(self, *args, **kwargs):
        """
        返回一个省份列表
        :param args: 
        :param kwargs: 
        :return: 
        """
        provinces = get_province()
        if provinces:
            self.write_json(provinces)
        else:
            self.send_error(500)
        return


class GetCity(BaseHandler):
    def post(self, *args, **kwargs):
        """
        根据province_id获取一个城市列表
        :param args: 
        :param kwargs: 
        :return: 
        """
        province_id = self.get_argument('province_id')
        if province_id:
            cities = get_city_id(province_id)
            if cities:
                self.write_json(cities)
            else:
                self.send_error(500)
            return
        self.send_error(400)
        return


class GetStation(BaseHandler):
    def post(self, *args, **kwargs):
        """
        根据city_id获取一个站点id列表
        :param args: 
        :param kwargs: 
        :return: 
        """
        province_id = self.get_argument('province_id')
        if not province_id:
            self.send_error(400)
        city_id = self.get_argument('city_id')
        if not city_id:
            self.send_error(400)
        self.write_json(get_station_id(province_id, city_id))
