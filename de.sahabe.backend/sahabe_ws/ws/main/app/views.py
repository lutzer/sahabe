'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import response

import qm.main.User  as userQM 
import qm.main.Password as passwordQM
import qm.main.Link as linkQM
import qm.main.LinkStorage as linkStoreQM

import common.main.converter.Link as linkConv
import common.main.converter.Tag as tagConv
import common.main.utils as utils

from flask import session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from ws.main.app import app, lm
import ast


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


@app.route("/load_links", methods=["GET", "POST"])
@login_required
def load_links():
#     try:
    upload = request.files["file"]
    user = g.user
    data = utils.extractData(upload)
    linkStoreQM.addJSONLinksByUser(data, user.id)
#     message = {"message":"%s links were added"%(links[0])}
#     return response.sendData([message] + links[1])
    return response.send200()
#     except Exception, e:
#         return response.send400("Error %s" %(e))
   

@app.route("/link/add", methods=["PUT"])
@login_required
def addLink():
    try:
        linkStoreQM.addLink(request.form, g.user.id)
        return response.send200("link added successfully")
    except Exception, e: 
        return response.send400("Error %s" %(e)) 
    

@app.route("/links", methods=["GET"])
@login_required
def links():
    try:
        linksSet = linkQM.getLinksByUserId(g.user.id)
        links = linkConv.convertLinksSetToDicts(linksSet)
        return response.sendData(links)
    except Exception, e:
        return response.send400("Error %s" %(e))


@app.route("/links/<linkId>", methods=["PUT"])
@login_required
def updateLink(linkId):

    data = ast.literal_eval(request.data)
    try:
        linkQM.update(data)
    except (Exception, ), e:
        return response.send400("Error %s" %(e))

    return response.send200("update successful")


@app.route("/links/<linkId>", methods=["DELETE"])
@login_required   
def deleteLink(linkId):
    affected = 0
    try:
        affected = linkQM.dropLinksbyUser(g.user.id, [linkId])
    except Exception, e:
        return response.send400("Error %s" %(e))
    
    if affected == 1:
        return response.send200("delete successful")
    elif affected == 0 :
        return response.send400("link not deleted")
    
    
@app.route("/links/delete", methods=["POST"])
@login_required   
def deleteLinks():
    
    linkIds=request.form.getlist("linkIds[]")

    if linkIds == []:
        return response.send200("list is empty")

    affected = 0
    
    try:
        affected = linkQM.dropLinksbyUser(g.user.id, linkIds)
    except Exception, e:
        return response.send400("Error %s" %(e))

    if affected == len(linkIds):
        return response.send200("delete successful")
    elif affected < len(linkIds) and affected > 0:  
        return response.send400("not all links could be deleted")
    elif affected == 0 :
        return response.send400("no links could be deleted")
    
    
@app.route("/links/drop_all", methods=["GET"])
def dropAllLinks():
    count = linkQM.dropAllLinksByUser(g.user.id)
    return response.send200("%s links dropped"%(count))

    
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
    results = [{"tags":tags},{"links":links}]
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
