'''
Created on Jul 22, 2014

@author: Maan Al Balkhi
'''
import time
import copy
import hashlib
import MetaData
import Link as linkQM
import Tag as tagQM
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
    
    return kwargs

def addJSONLinksByUser(data, userId):
    #FIXME: change insertion algorithm for sql queries that inserting data
    #as zip, json or ...
    #curTime = time.time()
    query = {"linksQuery":StringHolder("INSERT INTO link (id, user_id, url, url_hash, title, description, type_name, modified_at) VALUES\n"),
             "updateLinkSubQuery":{"id":StringHolder(""),
                                   "title":StringHolder(""),
                                   "description":StringHolder(""),
                                   "type_name":StringHolder(""),
                                   "modified_at":StringHolder("")},
             "tagsQuery":StringHolder("INSERT INTO tag (id, user_id, name) VALUES\n"),
             "mapsQuery":StringHolder("INSERT INTO link_tag_map (tag_id, link_id) VALUES\n"),
             "mdQuery":StringHolder("INSERT INTO meta_data (link_id, l_key, value) VALUES\n")}
    
    tags = []
    savedTags = tagQM.getTagNames(userId)
    savedLinks = linkQM.getLinkUrlsAndIds(userId)
    parseData(userId, data, tags, query, savedLinks, savedTags)
    
    #print "calculating time: " + str(utils.timeDifference(curTime)) + " ms"
    #curTime = time.time()
    
    conn = db.connect()
    cursor = conn.cursor()
    if not query["linksQuery"].value.endswith("VALUES\n"):
        cursor.execute(query["linksQuery"].value[:-2])
    if not query["mdQuery"].value.endswith("VALUES\n"):
        cursor.execute(query["mdQuery"].value[:-2])
    if not query["tagsQuery"].value.endswith("VALUES\n"):
        cursor.execute(query["tagsQuery"].value[:-2])
    #FIXME : check if link refer to another tag
    if not query["mapsQuery"].value.endswith("VALUES\n"):
        cursor.execute(query["mapsQuery"].value[:-2])
    if query["updateLinkSubQuery"]["id"].value != "":
        cursor.execute(buildUpdateQuery(query["updateLinkSubQuery"]))
    
    conn.commit()
    cursor.close()
    #print "database request time: " + str(utils.timeDifference(curTime)) + " ms"   
    return


class StringHolder():
    '''
    Used to save a String object over the recursive functions call 
    '''
    def __init__(self, value = ""):
        self.value = value
        
    def add(self, value):
        self.value += value

def parseData(userId, json_data, tags, query, savedLinks, savedTags):
        if "children" in json_data:
            if "title" in json_data:
                if not isTagInList(json_data["title"], savedTags):
                    tag = Tag.newTag(userId, json_data["title"])
                    query["tagsQuery"].add("('%s', '%s', '%s'),\n"%(tag.id, tag.userId, tag.name))
                    tags.append(tag)
            
            for child in json_data["children"]:
                ''' call by value '''
                tagsCopy = copy.copy(tags) 
                parseData(userId, child, tagsCopy, query, savedLinks, savedTags)
        else:
            if "title" in json_data and "uri" in json_data and not json_data["uri"].startswith("place:"):
                    savedLink = isUrlInList(json_data["uri"], savedLinks)
                    newLink = extractLink(userId, json_data)
                    if savedLink is None:
                        linkEntriesQuery(userId, newLink, json_data, tags, query)
                    else:
                        buildUpdateQueryCases(newLink, savedLink[0], query["updateLinkSubQuery"])
                        
def linkEntriesQuery(userId, newLink, json_data, tags, query):
        query["linksQuery"].add(buildLinkQuery(newLink))
        
        md = buildMetaDataQuery(json_data, newLink) 
        query["mdQuery"].add(md)
               
        linkTagsMap = buildLinkTagsMapQuery(tags, newLink.id) 
        query["mapsQuery"].add(linkTagsMap)

def isTagInList(tag, savedTags):
    for savedTag in savedTags:
        if type(tag) is unicode:
            tag = tag.encode("utf8") 
        if savedTag[0] == tag:
            return True
        
def isUrlInList(url, savedLinks):
    for savedLink in savedLinks:
        if savedLink[1] == url:
            return savedLink
    return None

def buildUpdateQuery(updateQueries):
    updateQuery = """UPDATE link SET title = CASE id %s END,
                                      description = CASE id %s END,
                                      type_name = CASE id %s END,
                                      modified_at = CASE id %s END
                                  WHERE id IN ( %s )
                  """%(updateQueries["title"].value,
                       updateQueries["description"].value,
                       updateQueries["type_name"].value,
                       updateQueries["modified_at"].value,
                       updateQueries["id"].value[:-2])
    return updateQuery

def buildUpdateQueryCases(newLink, savedLinkId, updateQueries):
    updateQueries["id"].add("'%s', "%(savedLinkId))
    updateQueries["title"].add("WHEN '%s' THEN '%s' "%(savedLinkId, newLink.title))
    updateQueries["description"].add("WHEN '%s' THEN '%s' "%(savedLinkId, newLink.description))
    updateQueries["type_name"].add("WHEN '%s' THEN '%s' "%(savedLinkId, newLink.typeName))
    updateQueries["modified_at"].add("WHEN '%s' THEN '%s' "%(savedLinkId, newLink.modifiedAt))

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

    description = ""
    if data.has_key("annos"):    
        description = data["annos"][0]["value"].replace("'", "")

    typeName= "uncategorized"

    lastModified = data["lastModified"]/1000000
    dtLastModified = utils.convertToDateTime(lastModified)
    
    return Link.newLink(userId, url, title, description, typeName, dtLastModified)
