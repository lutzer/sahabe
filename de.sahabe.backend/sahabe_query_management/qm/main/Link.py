'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

import uuid
import hashlib
import MetaData
from admin.main import DBApiModule as db
from common.main import utils
from datetime import datetime


def addLink(form, userId):
    linkId = str(uuid.uuid4())
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
    
    
    

def getLinksByUserId(userId):
    '''
    @param userId: user uuid 
    returns a set of a presentable link 
    '''
    conn = db.connect()
    resultSet = db.selectFrom(conn, {"link", "meta_data"},
                              "link.id",
                              "link.url",
                              "link.title",
                              "link.type_name",
                              "link.modified_at",
                              "meta_data.value",
                              user_id__IN__link=userId,
                              link_id__IN__meta_data="id__IN__link",
                              l_key__IN__meta_data="logo")
    #FIXME: select even there is no meta data entry
    return resultSet

def addLinksJSONFileByUser(data, userId):
    linksData = data["children"][0]["children"]
    links = []
    
    #FIXME: change insertion algorithm for sql queries that inserting data
    #as zip, json or ... 
    query = "INSERT INTO link (id, user_id, url, url_hash, title, type_name, modified_at) VALUES "
    mdQuery = "INSERT INTO meta_data (link_id, l_key, value) VALUES "
    for i in range(4, len(linksData)):
        if linksData[i].has_key("title") and linksData[i].has_key("uri"): 
            linkId = str(uuid.uuid4())
            url = linksData[i]["uri"]
            urlHash = hashlib.md5(url).hexdigest()
            title =  linksData[i]["title"].replace("'", "")
            lastModified = linksData[i]["lastModified"]/1000000
            dtLastModified = str(datetime.fromtimestamp(lastModified))
            typeName= "uncategorized"
            
            logo = utils.extractHomeUrl(url)+"favicon.ico"
            
            links.append({"id":linkId,
                        "title":title,
                        "url":url,
                        "typeName":typeName,
                        "modifiedAt":dtLastModified,
                        "logo":logo})
            
            query += "('%s', '%s', '%s', '%s', '%s', '%s', '%s'), "%(linkId,
                                                       userId,
                                                       url,
                                                       urlHash,
                                                       title,
                                                       typeName,
                                                       dtLastModified)
            
            mdQuery += "('%s', '%s', '%s'), "%(linkId,
                                         "logo",
                                         logo)
            
            print "url: " + url
            print "logo: " + logo
            print "-----------------"
            
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(query[:-2])
    cursor.execute(mdQuery[:-2])
    conn.commit()
    cursor.close()
    return (cursor.rowcount, links)


def searchLinkByUser(userId, searchValue):
    conn = db.connect()

    resultSet = db.selectFormWhereClause(conn, ["link","meta_data"],
                            ["link.id",
                             "link.url",
                             "link.title",
                             "link.type_name",
                             "link.modified_at",
                             "meta_data.value"],
                            "link.id",
                            db.Where("link.user_id", userId).equal(),
                            db.Where("meta_data.link_id", "id__IN__link").ANDEqual(),
                            db.Where("meta_data.l_key","logo").ANDEqual(),
                            db.Where("link.url", searchValue).ANDMatch(),
                            db.Where("link.title", searchValue).ORMatch(),
                            db.Where("link.description", searchValue).ORMatch(),
                            db.Where("link.type_name", searchValue).ORMatch())
    return resultSet
    

def dropAllLinksByUser(userId):
    conn = db.connect()
    count = db.deleteFromTable(conn, "link", user_id=userId)
    return count
            