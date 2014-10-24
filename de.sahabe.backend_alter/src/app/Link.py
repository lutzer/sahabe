'''
Created on Jul 24, 2014

@author: Maan Al Balkhi

get all:                /links                          - GET
search:                 /links?searchvalue=             - GET
add:                    /links                          - PUT
update:                 /links/<linkId>                 - POST
delete:                 /links/<linkId>                 - DELETE
multiple delete:        /links/delete                   - POST
import from a file:     /links/import                   - POST
'''

import ast
import response
from app.qm import Link as linkQM 
from app.qm import LinkStorage as linkStoreQM 

from app.common import utils
from app.common.converter import Tag as tagConv
from app.common.converter import Link as linkConv

from flask import request, g 
from flask_login import login_required
from app import app


@app.route("/links", methods=["GET"])
@login_required
def links():
    ''' Get all links if there is no argument, else do a search '''
    if request.args.items() == [] :
        try:
            linksSet = linkQM.getLinksByUserId(g.user.id)
        except Exception, e:
            return response.send400("Error %s" %(e))
        
        links = linkConv.convertLinksSetToDicts(linksSet)
        return response.sendData(links)
        
    else :
        searchValue = request.args["searchValue"]
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


@app.route("/links", methods=["POST"])
@login_required
def addLink():
    try:
        linkStoreQM.addLink(request.get_json(), g.user.id)
    except Exception, e: 
        return response.send400("Error %s" %(e)) 
    return response.send200("link added successfully")


@app.route("/links/<linkId>", methods=["PUT"])
@login_required
def updateLink(linkId):
    try:
        linkQM.update(request.get_json(), linkId)
    except (Exception, ), e:
        return response.send400("Error %s" %(e))

    return response.response200()


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


@app.route("/links/import", methods=["GET", "POST"])
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
