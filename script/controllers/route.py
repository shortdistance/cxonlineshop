# -*-coding:utf-8-*-
from . import main


@main.route('/')
def test():
    return "test"
