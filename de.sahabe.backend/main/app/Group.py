'''
Created on Oct 24, 2014

@author: Maan Al Balkhi

get all:                /groups            - GET
create:                 /groups/create     - PUT
get links by group      /groups/links      - POST
multiple delete         /groups/delete     - POST
'''

import response
from app.qm import Group as groupQM
from app.common.converter import Link as linkConv 
from app.common.converter import Group as groupConv

from flask import request, g 
from flask_login import login_required
from app import app


@app.route("/groups", methods=["GET"])
@login_required
def groups():
    try:
        groupsSet = groupQM.getGroupsByUser(g.user.id)
    except Exception, e:
        return response.send400("Error %s" %(e))
    groups = groupConv.converGroupsSetToDict(groupsSet)
    respData = {}
    respData["groups"] = groups 
    return response.sendData(respData)


@app.route("/groups/create", methods=["PUT"])
@login_required
def createGroup():
    name = request.form["name"]
    public = request.form["public"]
    try:
        groupQM.create(g.user.id, name, public)
    except Exception, e: 
        return response.send400("Error %s" %(e))
    return response.send200("group created successfully")


@app.route("/groups/delete", methods=["POST"])
@login_required   
def deleteGroups():
    groupIds=request.form.getlist("groupIds[]")

    if groupIds == []:
        return response.send200("list is empty")

    affected = 0
    
    try:
        affected = groupQM.deleteGroups(groupIds)
    except Exception, e:
        return response.send400("Error %s" %(e))

    if affected == len(groupIds):
        return response.send200("delete successful")
    elif affected < len(groupIds) and affected > 0:  
        return response.send400("not all links could be deleted")
    elif affected == 0 :
        return response.send400("no links could be deleted")
    

@app.route("/groups/links", methods=["POST"])
@login_required
def getGroupLinks():
    groupId = request.form["groupId"]
    try:
        linksSet = groupQM.getLinks(groupId)
    except Exception, e:
        return response.send400("Error %s" %(e))
    links = linkConv.convertLinksSetToDicts(linksSet)
    respData = {}
    respData["links"] = links
    return response.sendData(respData)
