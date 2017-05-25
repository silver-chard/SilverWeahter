#coding=utf-8


import os

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), "../../template"),
    'static_path': os.path.join(os.path.dirname(__file__), "../../static"),
    'ports': 8888,
    'debug': True,
}