from tornado import gen

from handlers.basehandlers.basehandler import BaseHandler


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render_string('index.html')
