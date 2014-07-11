'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

app = Flask(__name__)
app.config.from_object("config")
lm = LoginManager()
lm.init_app(app)
#lm.login_view = "login"
lm.login_message = "Please log in to access this page."
lm.login_message_category = "info" #allowed categories: error, info, message and warning
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views