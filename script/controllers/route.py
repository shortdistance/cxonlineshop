# -*-coding:utf-8-*-
from . import main
from flask import url_for, request, render_template


@main.route('/')
def index():
    return render_template("details.html")


@main.route('/ping')
def ping():
    return "ping OK!"

