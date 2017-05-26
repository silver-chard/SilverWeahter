# coding=utf-8
import logging

import tornado
from tornado import web, options, httpserver, ioloop

from web.sys.config.settings import settings
from web.sys.urls import url_patterns


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)


if __name__ == '__main__':
    logging.info('Tornado is running')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(settings['ports'])
    tornado.ioloop.IOLoop.instance().start()
