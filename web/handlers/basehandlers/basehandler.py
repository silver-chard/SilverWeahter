# coding=utf-8
import json
import logging

import mako.lookup
import mako.template
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        template_path = self.get_template_path()
        self.lookup = mako.lookup.TemplateLookup(
            directories=[template_path], input_encoding='utf-8', output_encoding='utf-8')

    def render_string(self, template_path, **kwargs):

        try:
            template = self.lookup.get_template(template_path)
            namespace = self.get_template_namespace()
            namespace.update(kwargs)

            # siteConfig=WebConfig()
            env_kwargs = dict(
                debug=self.get_argument("debug", "false"),
                handler=self,
                request=self.request,
                locale=self.locale,
                static_url=self.static_url,
                reverse_url=self.application.reverse_url,
                user_agent=self.request.headers["User-Agent"]
            )
            env_kwargs.update(kwargs)
            self.write(template.render(**env_kwargs))
        except Exception as e:
            logging.error("服务端错误  {e}".format(e=e))

    def render(self, template_path, **kwargs):
        self.finish(self.render_string(template_path, **kwargs))

    def write_json(self, obj, cls=None, **kwargs):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json.dumps(obj, cls=cls, **kwargs))
