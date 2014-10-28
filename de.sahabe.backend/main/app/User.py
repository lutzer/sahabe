'''
Created on Jul 4, 2014

@author: Maan Al Balkhi

get user data  /user/data   - GET
sign up:       /sign_up     - GET, POST
login:         /login       - POST
logout:        /logout      - GET
'''

import response

from app.qm import User as userQM 
from app.qm import Password as passwordQM
from app.common.converter import User as userConv 

from flask import session, request, g
from flask_login import login_required, login_user, logout_user, current_user
from app import app, lm


''' RESTApi interface '''

@app.route("/user/data", methods=["GET"])
@login_required
def getUser():
    try:
        resultSet = userQM.getUserById(g.user.id)
        user = userConv.converUserToDict(resultSet)
        respData = {}
        respData["user"] = user
        return response.sendData(respData)
    except Exception, e:
        return response.send400("Error %s" %(e))
    
    
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
        
        if user != None and user != False:
            session["remember_me"] = remember_me
            login_user(user, remember_me)
            app.logger.info("user: %s logged in "%(user.username))
            return response.sendData(userConv.converUserToDict(user))
        else:
            return response.send401("incorrect password or user name")
    
    except Exception, e:
        return response.send400("Error %s" %(e))
    

@app.route('/logout')
def logout():
    try:
        logout_user()
        print "logged out"
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
