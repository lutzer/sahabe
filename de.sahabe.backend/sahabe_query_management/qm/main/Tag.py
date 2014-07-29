'''
Created on Jul 15, 2014

@author: Maan Al Balkhi
'''

import uuid
from db.main import DBApiModule as db

def create(userId, name):
    conn = db.connect()
    count = db.insertToTable(conn, "tag", id=str(uuid.uuid4()), name=name, user_id=userId)
    return count

def tagLink(linkId, tagId):
    conn = db.connect()
    count = db.insertToTable(conn, "link_tag_map", tag_id=tagId, link_id=linkId)
    return count

def getTagsByUser(userId):
    conn = db.connect()
    resultSet = db.selectFrom(conn, {"tag"}, "id", "name", user_id=userId)
    return resultSet

def deleteTags(tagIds):
    query = "delete from tag where "
    for _id in tagIds:
        query += " id='%s' or\n"%(_id)
    query = query[:-4]
    conn = db.connect()
    cursor = conn.cursor()
    affected = cursor.execute(query)
    conn.commit()
    cursor.close()
    return affected

def getLinks(tagId):

    query = """SELECT link.id, link.url, link.title, link.description, link.type_name, link.modified_at, md.value
FROM meta_data AS md
JOIN link ON link.id = md.link_id AND link.id IN
(SELECT link_id FROM link_tag_map WHERE tag_id = '%s')"""%(tagId)

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    links = cursor.fetchall()
    conn.commit()
    cursor.close()
    return links
