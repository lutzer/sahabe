'''
Created on Jul 4, 2014

@author: Maan Al Balkhi

index:         /            - GET
               /index       - GET
sign up:       /sign_up     - GET, POST
search:        /search      - POST
login:         /login       - POST
logout:        /logout      - GET
'''

import response

from qm.main import User as userQM 
from qm.main import Password as passwordQM 
from qm.main import Link as linkQM 

from common.main.converter import Link as linkConv 
from common.main.converter import Tag as tagConv 

from flask import session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from ws.main.app import app, lm


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


@app.route("/")
@app.route("/index")
@login_required
def index():
    try:
        user = g.user
        dbLinks = linkQM.getLinksByUserId(user.id)
        links = linkConv.convertLinksSetToDicts(dbLinks)
        return response.sendData(links)
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

    
@app.route("/search", methods=["POST"])
@login_required
def search():
    if request.form["searchValue"] == "":
        return response.sendData([])
    searchValue = request.form["searchValue"]
    
    try:
        searchResults = linkQM.searchLinkByUser(g.user.id, searchValue)
    except Exception, e:
        return response.send400("Error %s" %(e)) 
    
    tags = tagConv.converTagsSetToDict(searchResults[0])
    links = linkConv.convertLinksSetToDicts(searchResults[1])
    results = {}
    results["tags"]=tags
    results["links"]=links
    return response.sendData(results)
    

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
      

@lm.unauthorized_handler
def unauthorized():
    return response.send401("login required")
