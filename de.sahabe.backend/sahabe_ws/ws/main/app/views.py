'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import response

import qm.main.User  as userQM 
import qm.main.Password as passwordQM
import qm.main.Link as linkQM

import common.main.converter.Link as linkConv
import common.main.utils as utils

from flask import session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from ws.main.app import app, lm


@lm.user_loader
def load_user(_id):
    return userQM.getUserById(_id)


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


@app.route("/load_links", methods=["GET", "POST"])
@login_required
def load_links():
    try:
        upload = request.files["file"]
        user = g.user
        data = utils.extractData(upload)
        links = linkQM.addLinksJSONFileByUser(data, user.id)
        message = {"message":"%s links were added"%(links[0])}
        return response.sendData([message] + links[1])
    except Exception, e:
        return response.send400("Error %s" %(e))
   

@app.route("/link/add", methods=["PUT"])
@login_required
def addLink():
    try:
        linkQM.addLink(request.form, g.user.id)
        return response.send200("link added successfully")
    except Exception, e: 
        return response.send400("Error %s" %(e)) 
    

@app.route("/links", methods=["GET", "POST"])
@login_required
def getAllLinks():
    try:
        linksSet = linkQM.getLinksByUserId(g.user.id) 
        links = linkConv.convertLinksSetToDicts(linksSet)
        return response.sendData(links)
    except Exception, e:
        return response.send400("Error %s" %(e))

@app.route("/links/drop_all", methods=["GET"])
def dropAllLinks():
    count = linkQM.dropAllLinksByUser(g.user.id)
    return response.send200("%s links dropped"%(count))
    
@app.route("/search", methods=["POST"])
@login_required
def search():
    searchValue = request.form["searchValue"]
    linksSet = linkQM.searchLinkByUser(g.user.id, searchValue)
    count = len(linksSet)
    message = {"message":"%s links found"%(count)}
    links = linkConv.convertLinksSetToDicts(linksSet)
    return response.sendData([message]+links)
    

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
