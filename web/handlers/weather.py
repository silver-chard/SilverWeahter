import ConfigParser
import datetime

from handlers.basehandlers.basehandler import BaseHandler
from robot.IronManSuits.suits import MarkI


class GetWeatherHandler(BaseHandler):
    def get(self, city_id, *args, **kwargs):
        city_id = int(city_id)
        weather_date = self.get_argument('weather_date',
                                         (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%M-%d'))
        weather_time = self.get_argument('weather_time', 255)
        # conf = ConfigParser.ConfigParser()
        # conf.read("../robot/config/config.ini")
        #
        # robot = MarkI(city_id, conf)
        # robot.get_data()
        # print robot.weather_data
        # {
        #     'city_id': city_id,
        #     'weather_date': weather_date,
        #     'weather_time': weather_time
        # }

        self.write_json({
            'city_id': city_id,
            'weather_date': weather_date,
            'weather_time': 8,
            'cond': 0,
            'temp': 23,
            'wind_dir': 4,
            'wind_speed': 0,
        })
