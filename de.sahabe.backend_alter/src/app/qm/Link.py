'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

from app.db import DBApiModule as db
from app.common import utils


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
                              "link.description",
                              "link.type_name",
                              "link.modified_at",
                              "meta_data.value",
                              user_id__IN__link=userId,
                              link_id__IN__meta_data="id__IN__link",
                              l_key__IN__meta_data="iconUrl")
    return resultSet

def searchLinkByUser(userId, searchValue):
    
    searchLinks="""
SELECT link.id, link.url, link.title, link.description, link.type_name, link.modified_at, md.value
FROM meta_data AS md
JOIN link ON link.id = md.link_id AND link.id IN 
(SELECT l.id FROM link AS l WHERE
l.user_id='%s' AND %s OR %s OR %s OR %s)
"""%(userId,
     __buildRegexSearchClause("l.url",searchValue),
     __buildRegexSearchClause("l.title",searchValue),
     __buildRegexSearchClause("l.description",searchValue),
     __buildRegexSearchClause("l.type_name",searchValue))
    
    searchTags="""SELECT id, name FROM tag WHERE %s """%(__buildRegexSearchClause("name", searchValue))
    
    conn = db.connect()
    cursor = conn.cursor()
    
    cursor.execute(searchLinks)
    links = cursor.fetchall()
    
    cursor.execute(searchTags)
    tags = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    return (tags, links)

def update(link, linkId):
    conn = db.connect()
    updateEntry = {}
    if link.has_key("url") and link["url"] != None:
        updateEntry["url"] = link["url"]
    if link.has_key("title") and link["title"] != None:
        updateEntry["title"] = link["title"]
    if link.has_key("description") and link["description"] != None:
        updateEntry["description"] = link["description"]
    if link.has_key("typeName") and link["typeName"] != None:
        updateEntry["type_name"] = link["typeName"]
    updateEntry["modified_at"] = utils.timeStamp()
    count = db.updateInTable(conn,
                             updateEntry,       
                             "link",
                             id=linkId)
    return count

def dropLinksbyUser(userId, linkIds):
    
    idsClause = ""
    for _id in linkIds:
        idsClause += " id='%s' or\n"%(_id)
    idsClause = idsClause[:-4]
    query = "delete from link where user_id='%s' and \n"%(userId) + idsClause 
    conn = db.connect()
    cursor = conn.cursor()
    affected = cursor.execute(query)
    conn.commit()
    cursor.close()
    return affected
    
def dropAllLinksByUser(userId):
    conn = db.connect()
    count = db.deleteFromTable(conn, "link", user_id=userId)
    return count

def __buildRegexSearchClause(column, searchValue):
    split = searchValue.split(" ")
    searchString = ""
    for word in split:
        if word!= "":
            searchString += "%s REGEXP '%s' AND "%(column, word)
    return searchString[:-4]
            