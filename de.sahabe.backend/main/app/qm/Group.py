'''
Created on Oct 24, 2014

@author: Maan Al Balkhi
'''

import uuid
from app.db import DBApiModule as db

def create(userId, name, public):
    conn = db.connect()
    
    if public == "true":
        public = "1"
    else:
        public = "0"
        
    count = db.insertToTable(conn, "link_group", id=str(uuid.uuid4()), user_id=userId, name=name, public=public)
    return count

def groupLink(linkId, groupId):
    conn = db.connect()
    count = db.insertToTable(conn, "link_group_map", group_id=groupId, link_id=linkId)
    return count

def getGroupsByUser(userId):
    conn = db.connect()
    resultSet = db.selectFrom(conn, {"link_group"}, "id", "name", "public", user_id=userId)
    return resultSet

def deleteGroups(groupIds):
    query = "delete from link_group where "
    for _id in groupIds:
        query += " id='%s' or\n"%(_id)
    query = query[:-4]
    conn = db.connect()
    cursor = conn.cursor()
    affected = cursor.execute(query)
    conn.commit()
    cursor.close()
    return affected

def getLinks(groupId):

    query = """SELECT link.id, link.url, link.title, link.description, link.type_name, link.modified_at, md.value
FROM meta_data AS md
JOIN link ON link.id = md.link_id AND link.id IN
(SELECT link_id FROM link_group_map WHERE group_id = '%s')"""%(groupId)

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    links = cursor.fetchall()
    conn.commit()
    cursor.close()
    return links
