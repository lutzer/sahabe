'''
Created on Jul 23, 2014

@author: Maan Al Balkhi
'''
import response
import qm.main.Tag as tagQM 
import common.main.converter.Tag as tagConv

from flask import request, g 
from flask_login import login_required
from ws.main.app import app


@app.route("/tags", methods=["GET"])
@login_required
def tags():
    try:
        tagsSet = tagQM.getTagsByUser(g.user.id)
    except Exception, e:
        return response.send400("Error %s" %(e))
    tags = tagConv.converTagsSetToDict(tagsSet)
    return response.sendData(tags)


@app.route("/tags/create", methods=["PUT"])
@login_required
def createTag():
    name = request.form["name"]
    try:
        tagQM.create(g.user.id, name)
    except Exception, e: 
        return response.send400("Error %s" %(e))
    return response.send200("tag created successfully")
    