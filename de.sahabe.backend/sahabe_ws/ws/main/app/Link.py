'''
Created on Jul 24, 2014

@author: Maan Al Balkhi

get all:             /links           - GET
load from a file:    /load_links      - GET, POST
add:                 /link/add        - PUT
update:              /links/<linkId>  - PUT
delete:              /links/<linkId>  - DELETE
multiple delete:     /links/delete    - POST
delete all           /links/drop_all  - GET
'''

import ast
import response
from qm.main import Link as linkQM 
from qm.main import LinkStorage as linkStoreQM 

from common.main import utils
from common.main.converter import Link as linkConv

from flask import request, g 
from flask_login import login_required
from ws.main.app import app


@app.route("/load_links", methods=["GET", "POST"])
@login_required
def load_links():
    upload = request.files["file"]
    user = g.user
    data = utils.extractData(upload)
    try:
        linkStoreQM.addJSONLinksByUser(data, user.id)
    except Exception, e:
        return response.send400("Error %s" %(e))
    return response.send200()

@app.route("/link/add", methods=["PUT"])
@login_required
def addLink():
    try:
        linkStoreQM.addLink(request.form, g.user.id)
    except Exception, e: 
        return response.send400("Error %s" %(e)) 
    return response.send200("link added successfully")
    

@app.route("/links", methods=["GET"])
@login_required
def links():
    try:
        linksSet = linkQM.getLinksByUserId(g.user.id)
    except Exception, e:
        return response.send400("Error %s" %(e))
    
    links = linkConv.convertLinksSetToDicts(linksSet)
    return response.sendData(links)
    

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
        #user id is required to verify that link belongs to a logged user.  
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
    try:
        count = linkQM.dropAllLinksByUser(g.user.id)
    except Exception, e:
        return response.send400("Error %s" %(e))
    return response.send200("%s links dropped"%(count))
