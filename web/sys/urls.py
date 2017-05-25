from handlers.index import IndexHandler
from handlers.weather import GetWeatherHandler

url_patterns = [
    ('/', IndexHandler),
    ('/index', IndexHandler),
    (r'/weather/data/([0-9]+)', GetWeatherHandler),
]
