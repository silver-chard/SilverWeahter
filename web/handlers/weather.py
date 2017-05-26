import datetime

from handlers.basehandlers.basehandler import BaseHandler
from services.weather import get_data


class GetWeatherHandler(BaseHandler):
    def get(self, *args, **kwargs):
        city_id = self.get_argument('city_id')
        weather_date = self.get_argument('weather_date')
        weather_date = weather_date.split(',')
        weather_time = self.get_argument('weather_time', 255)
        result = []
        for weather_d in weather_date:
            result = result + get_data(city_id, weather_d, weather_time)

        self.render_string('weather_table.html', result=result)
