# -*-coding:utf-8-*-
from . import main


@main.route('/test')
def test():
    return "test OK!"


@main.route('/ping')
def ping():
    return "ping OK!"

