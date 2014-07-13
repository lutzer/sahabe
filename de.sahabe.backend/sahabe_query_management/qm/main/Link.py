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
    count = 0
    links = []
    
    #FIXME: change insertion algorithm for sql queries that inserting data
    #as zip, json or ... 
    
    for i in range(4, len(linksData)):
        if linksData[i].has_key("title") and linksData[i].has_key("uri"): 
            title =  linksData[i]["title"].replace("'", "")
            url = linksData[i]["uri"]
            
            lastModified = linksData[i]["lastModified"]/1000000
            dtLastModified = str(datetime.fromtimestamp(lastModified))
            
            logo = utils.extractHomeUrl(url)+"favicon.ico"
            
            linkId = str(uuid.uuid4())
            links.append({"id":linkId,
                          "title":title,
                          "url":url,
                          "typeName":"",
                          "modifiedAt":dtLastModified,
                          "logo":logo})

            conn = db.connect()
            db.insertToTable(conn, "link",
                             id = linkId,
                             user_id = userId,
                             title = title,
                             url = url,
                             url_hash = hashlib.md5(url).hexdigest(),
                             modified_at = dtLastModified)
            
            MetaData.addLogo(linkId, logo)
            count += 1
    return (count, links)


def searchLinkByUser(userId, searchValue, groupBy):
    conn = db.connect()
    
#     kwargs = {}
#     kwargs["user_id__IN__link"] = userId 
#     kwargs["link_id__IN__meta_data"] = "id__IN__link"
#     kwargs["l_key__IN__meta_data"] = "logo"
#     
#     
#     
#     resultSet = db.selectFrom(conn, {"link", "meta_data"}, True,
#                               "link.id",
#                               "link.url",
#                               "link.title",
#                               "link.type_name",
#                               "link.modified_at",
#                               "meta_data.value",
#                               **kwargs)

    """ WHERE FOR search_table """

#                             db.Where("search_table.groups", searchValue).ORLike(),
#                             db.Where("search_table.tags", searchValue).ORLike(),
#                             db.Where("search_table.text", searchValue).ORLike()
#                             db.Where("search_table.link_id", "id__IN__link").OREqual(),
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
                            db.Where("link.url", searchValue).ANDLike(),
                            db.Where("link.title", searchValue).ORLike(),
                            db.Where("link.description", searchValue).ORLike(),
                            db.Where("link.type_name", searchValue).ORLike())
    return resultSet
    









            
            
            
            