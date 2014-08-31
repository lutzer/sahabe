'''
Created on Jul 4, 2014

@author: Maan Al Balkhi

sign up:       /sign_up     - GET, POST
login:         /login       - POST
logout:        /logout      - GET
'''

import response

from qm.main import User as userQM 
from qm.main import Password as passwordQM 

from flask import session, request, g
from flask_login import login_user, logout_user, current_user
from ws.main.app import app, lm


''' RESTApi interface '''

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    try:
        userId = userQM.createUser(request.form)
        passwordQM.createPasswordForUser(userId, request.form["password"])
        return response.send200("You signed up successfully")
    except Exception, e:
        return response.send400("Error %s" %(e))


@app.route("/login", methods=["POST"])
def login():
    try:
        name = request.form["username"]
        password = request.form["password"]
        remember_me = request.form["remember"]
        
        user = userQM.authenticate(name, password)
        
        session["remember_me"] = remember_me
        login_user(user, remember_me)
        app.logger.info("user: %s logged in "%(user.nickname))
        return response.send200("Logged in successfully")
    except Exception, e:
        return response.send400("Error %s" %(e))
    

@app.route('/logout')
def logout():
    try:
        logout_user()
        return response.send200("logout was successful")
    except Exception, e:
        return response.send400("Error %s" %(e))
    
    
''' Authorization management '''

@lm.user_loader
def load_user(_id):
    try:
        return userQM.getUserById(_id)
    except Exception, e:
        #FIXME: not every exception should remove the session
        session.pop(_id, None)
        return response.send400("Error %s" %(e))

@app.before_request
def before_request():
    g.user = current_user

@lm.unauthorized_handler
def unauthorized():
    return response.send401("login required")
