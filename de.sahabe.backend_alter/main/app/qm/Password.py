'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

import hashlib
from app.db import DBApiModule as db


def getPasswordByUserId(userId):
    conn = db.connect()
    rows = db.selectFrom(conn, {"pw_hash"}, "value", user_id = userId)
    return rows[0][0]

def createPasswordForUser(userId, password):
    conn = db.connect()
    value = hashlib.sha256(password).hexdigest()
    salt = hashlib.sha256(value+userId).hexdigest()
    db.insertToTable(conn, "pw_hash",
                     user_id=userId,
                     value=value,
                     salt=salt)
    return True
