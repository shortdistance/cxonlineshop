# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from script.config import SECRET_KEY, DEBUG
from flask_dropzone import Dropzone


mail = Mail()
dropzone = Dropzone()

def create_app():
    app = Flask(__name__)
    app.debug = DEBUG

    # load config file
    app.config.from_pyfile('config.py')

    # config secret key
    app.config['SECRET_KEY'] = SECRET_KEY

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    # init app by mail
    mail.init_app(app)
    dropzone.init_app(app)

    from script.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from script.controllers import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app


class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)
