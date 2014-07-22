'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

from db.main import DBApiModule as db
from common.main import utils


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
#    searchString = searchValue.replace(" ", ".+")
    
#     split = searchValue.split(" ")
#     searchString = ""
#     for word in split:
#         searchString +="(?=.*\%s\b)"%(word) 
#         
#     searchString = "^%s.+"%(searchString)
    
#     regexSearch="""select link.id, link.url, link.title, link.type_name, link.modified_at, md.value from meta_data as md
# join link on link.id = md.link_id  and link.id in 
# (select l.id from link as l where
# l.user_id='%s' and 
# l.url REGEXP '%s' or
# l.title REGEXP '%s' or
# l.description REGEXP '%s' or
# l.type_name REGEXP '%s')
# """%(userId, searchString, searchString, searchString, searchString)
#     
#     conn = db.connect()
#     cursor = conn.cursor()
#     cursor.execute(regexSearch)
# 
#     rows = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     print len(rows)
#     return rows
    
    def buildRegexSearchClause(column, searchValue):
        split = searchValue.split(" ")
        searchString = ""
        for word in split:
            if word!= "":
                searchString += "%s REGEXP '%s' and "%(column, word)
        return searchString[:-4]
    
    regexSearch="""select link.id, link.url, link.title, link.description, link.type_name, link.modified_at, md.value from meta_data as md
join link on link.id = md.link_id  and link.id in 
(select l.id from link as l where
l.user_id='%s' and 
 %s or
 %s or
 %s or
 %s)
"""%(userId,
     buildRegexSearchClause("l.url",searchValue),
     buildRegexSearchClause("l.title",searchValue),
     buildRegexSearchClause("l.description",searchValue),
     buildRegexSearchClause("l.type_name",searchValue))
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(regexSearch)

    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    return rows

def update(link):
    conn = db.connect()
    count = db.updateInTable(conn,
                     {"url":link["url"],
                      "title":link["title"],
                      "description":link["description"],
                      "type_name":link["typeName"],
                      "modified_at":utils.timeStamp()},
                     "link",
                     id=link["linkId"])
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
            