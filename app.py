# -*- coding: utf-8 -*-
from flask import Flask
from views import _pages
from config import config
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(_pages)
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    app.run(port=5000)
