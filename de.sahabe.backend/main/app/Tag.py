'''
Created on Jul 23, 2014

@author: Maan Al Balkhi

get all:            /tags            - GET
create:             /tags/create     - PUT
get links by tag    /tags/links      - POST
multiple delete     /tags/delete     - POST
'''

import response
from app.qm import Tag as tagQM
from app.common.converter import Link as linkConv 
from app.common.converter import Tag as tagConv 

from flask import request, g 
from flask_login import login_required
from app import app


@app.route("/tags", methods=["GET"])
@login_required
def tags():
    try:
        tagsSet = tagQM.getTagsByUser(g.user.id)
    except Exception, e:
        return response.send400("Error %s" %(e))
    tags = tagConv.converTagsSetToDict(tagsSet)
    respData = {}
    respData["tags"] = tags
    return response.sendData(respData)


@app.route("/tags/create", methods=["PUT"])
@login_required
def createTag():
    name = request.form["name"]
    try:
        tagQM.create(g.user.id, name)
    except Exception, e: 
        return response.send400("Error %s" %(e))
    return response.send200("tag created successfully")


@app.route("/tags/delete", methods=["POST"])
@login_required   
def deleteTags():
    tagIds=request.form.getlist("tagIds[]")

    if tagIds == []:
        return response.send200("list is empty")

    affected = 0
    
    try:
        affected = tagQM.deleteTags(tagIds)
    except Exception, e:
        return response.send400("Error %s" %(e))

    if affected == len(tagIds):
        return response.send200("delete successful")
    elif affected < len(tagIds) and affected > 0:  
        return response.send400("not all links could be deleted")
    elif affected == 0 :
        return response.send400("no links could be deleted")
    

@app.route("/tags/links", methods=["POST"])
@login_required
def getTagLinks():
    tagId = request.form["tagId"]
    try:
        linksSet = tagQM.getLinks(tagId)
    except Exception, e:
        return response.send400("Error %s" %(e))
    links = linkConv.convertLinksSetToDicts(linksSet)
    respData = {}
    respData["links"] = links
    return response.sendData(respData)