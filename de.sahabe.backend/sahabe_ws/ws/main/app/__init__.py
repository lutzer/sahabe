'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import os
from flask import Flask
from flask_login import LoginManager
from ws.main.config import basedir

app = Flask(__name__)
app.config.from_object("config")
lm = LoginManager()
lm.init_app(app)

#from ws.main.app import views
import views