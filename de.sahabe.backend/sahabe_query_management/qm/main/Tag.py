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
