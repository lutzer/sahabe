'''
Created on Jul 22, 2014

@author: Maan Al Balkhi
'''

import hashlib
import MetaData
from common.main import utils
from db.main import DBApiModule as db


def addLink(form, userId):
    linkId = utils.uuid()
    kwargs = {}
    kwargs["id"] = linkId
    
    kwargs["user_id"] = userId
    
    if form.has_key("url") :
        kwargs["url"]=form["url"]
        kwargs["url_hash"] = hashlib.md5(kwargs["url"]).hexdigest() 
    else:
        raise Exception("an url must be added")

    if form.has_key("title"): 
        kwargs["title"]=form["title"] 
    
    if form.has_key("description"):
        kwargs["description"]=form["description"]
        
    if form.has_key("typeName"):
        kwargs["type_name"]=form["typeName"]
    
    kwargs["modified_at"]=utils.timeStamp()
    
    #FIXME use other algorithms to get icon logo
    logo = utils.extractHomeUrl(kwargs["url"])+"favicon.ico"

    conn = db.connect()
    db.insertToTable(conn,
                     "link",
                    **kwargs)
    MetaData.addLogo(linkId, logo)
    
    return linkId


def addJSONLinksByUser(data, userId):
    #FIXME: change insertion algorithm for sql queries that inserting data
    #as zip, json or ...
    
    
    
       
    return 
