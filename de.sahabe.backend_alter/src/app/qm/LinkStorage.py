'''
Created on Jul 22, 2014

@author: Maan Al Balkhi
'''

import copy
import hashlib
import MetaData
from app.common import utils
from app.db import DBApiModule as db
from app.mytypes.Link import Link
from app.mytypes.Tag import Tag


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
    iconUrl = utils.extractHomeUrl(kwargs["url"])+"favicon.ico"

    conn = db.connect()
    db.insertToTable(conn,
                     "link",
                    **kwargs)
    MetaData.addIconUrl(linkId, iconUrl)
    
    return linkId

def addJSONLinksByUser(data, userId):
    #FIXME: change insertion algorithm for sql queries that inserting data
    #as zip, json or ...
    query = {"linksQuery":StringHolder("INSERT INTO link (id, user_id, url, url_hash, title, description, type_name, modified_at) VALUES\n"),
         "tagsQuery":StringHolder("INSERT INTO tag (id, user_id, name) VALUES\n"),
         "mapsQuery":StringHolder("INSERT INTO link_tag_map (tag_id, link_id) VALUES\n"),
         "mdQuery":StringHolder("INSERT INTO meta_data (link_id, l_key, value) VALUES\n")}
    
    tags = []
    parseData(userId, data, tags, query)
    
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(query["linksQuery"].value[:-2])
    cursor.execute(query["mdQuery"].value[:-2])
    cursor.execute(query["tagsQuery"].value[:-2])
    cursor.execute(query["mapsQuery"].value[:-2])
    conn.commit()
    cursor.close()
       
    return


class StringHolder():
    def __init__(self, value = ""):
        self.value = value
        
    def add(self, value):
        self.value += value

def parseData(userId, json_data, tags, query):
        if "children" in json_data:
            if "title" in json_data:
                
                tag = Tag.newTag(userId, json_data["title"])
                query["tagsQuery"].add("('%s', '%s', '%s'),\n"%(tag.id, tag.userId, tag.name))
                tags.append(tag)
            
            for child in json_data["children"]:
                ''' call by value '''
                tagsCopy = copy.copy(tags) 
                parseData(userId, child, tagsCopy, query)
        else:
            if "title" in json_data:
                linkEntriesQuery(userId, json_data, tags, query)
                
def linkEntriesQuery(userId, data, tags, query):
    if "uri" in data and not data["uri"].startswith("place:"):
        
        link = extractLink(userId, data)
        query["linksQuery"].add(buildLinkQuery(link))
        
        md = buildMetaDataQuery(data, link) 
        query["mdQuery"].add(md)
               
        linkTagsMap = buildLinkTagsMapQuery(tags, link.id) 
        query["mapsQuery"].add(linkTagsMap)

def buildLinkTagsMapQuery(tags, linkId):    
    values = ""
    for tag in tags:
        values += "('%s', '%s'),\n"%(tag.id, linkId)
    return values    
    
def buildMetaDataQuery(data, link):
    if data.has_key("iconuri"):
        iconUrl = data["iconuri"]
    else:
        iconUrl = utils.extractHomeUrl(link.url)+"favicon.ico"
    
    return "('%s', '%s', '%s'),\n"%(link.id, "iconUrl", iconUrl)
    

def buildLinkQuery(link):
    linkQuery = ("('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'),\n"
                 %(link.id,
                   link.userId,
                   link.url,
                   hashlib.md5(link.url).hexdigest(),
                   link.title,
                   link.description,
                   link.typeName,
                   link.modifiedAt))
    return linkQuery 

        
def extractLink(userId, data):
    url = data["uri"]
    title = data["title"].replace("'", "")

    description = "no_description"
    if data.has_key("annos"):    
        description = data["annos"][0]["value"].replace("'", "")
        if description == "":
            description = "no_description"

    typeName= "uncategorized"

    lastModified = data["lastModified"]/1000000
    dtLastModified = utils.convertToDateTime(lastModified)
    
    return Link.newLink(userId, url, title, description, typeName, dtLastModified)
