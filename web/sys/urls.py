from handlers.city import GetCity, GetProvince, GetStation
from handlers.index import IndexHandler
from handlers.weather import GetWeatherHandler

url_patterns = [
    ('/', IndexHandler),
    ('/index', IndexHandler),
    ('/get_data', GetWeatherHandler),
    ('/get_provinces', GetProvince),
    ('/get_cities', GetCity),
    ('/get_stations', GetStation),
]
