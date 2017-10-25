from flask import Blueprint
from script.models.db import db_session

main = Blueprint('main', __name__)

from . import route

@main.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Domain', '*')

    return response


"""
@main.after_request
def close_session_after_request(response):
    db_session.remove()
    return response
"""
