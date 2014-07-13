'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

import uuid
import hashlib

from admin.main import DBApiModule as db
from qm.main import Password as passwordQM
from mytypes.main.User import User



def getUserById(_id):
    conn = db.connect()
    rows = db.selectFrom(conn, {"user"}, "*", id = _id)
    return User(rows)
    
def getUserByName(name):
    conn = db.connect()
    rows = db.selectFrom(conn, {"user"}, "*", name = name)
    if rows == []:
        raise Exception("user not found")
    return User(rows)

def createUser(userForm):
    conn = db.connect()
    userId = str(uuid.uuid4())
    db.insertToTable(conn, "user",
                     id=userId,
                     name=userForm["username"],
                     email=userForm["email"])
    return userId

def authenticate(name, password):
    user = getUserByName(name)
    saved = passwordQM.getPasswordByUserId(user.id)
    generated = hashlib.sha256(password).hexdigest()
    if saved == generated:
        return user
    else:
        raise Exception("incorrect password or user name")
        
    
    
    
    
    
    
    
    
    