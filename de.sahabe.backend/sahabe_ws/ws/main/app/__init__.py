'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import os
from flask import Flask
from flask_login import LoginManager
from ws.main import config

app = Flask(__name__)
app.config.from_object("config")


if not config.debug:
    
    import logging
    from logging.handlers import RotatingFileHandler
    
    file_handler = RotatingFileHandler(config.log, 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')


lm = LoginManager()
lm.init_app(app)

#from ws.main.app import views
import views