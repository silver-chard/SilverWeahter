# coding=utf-8
from handlers.basehandlers.basehandler import BaseHandler
from services.city import get_province


class GetProvince(BaseHandler):
    def post(self, *args, **kwargs):
        """
        返回一个省份列表
        :param args: 
        :param kwargs: 
        :return: 
        """
        self.write_json(get_province())
        return


class GetCity(BaseHandler):
    def post(self, *args, **kwargs):
        """
        根据province_id获取一个城市列表
        :param args: 
        :param kwargs: 
        :return: 
        """
        pass


class GetStation(BaseHandler):
    def post(self, *args, **kwargs):
        """
        根据city_id获取一个站点id列表
        :param args: 
        :param kwargs: 
        :return: 
        """
        pass
