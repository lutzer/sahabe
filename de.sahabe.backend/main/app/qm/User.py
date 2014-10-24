'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

import uuid
import hashlib

from app.db import DBApiModule as db
from app.qm import Password as passwordQM
from app.mytypes.User import User



def getUserById(_id):
    conn = db.connect()
    rows = db.selectFrom(conn, {"user"}, "*", id = _id)
    return User(rows)
    
def getUserByName(name):
    conn = db.connect()
    rows = db.selectFrom(conn, {"user"}, "*", name = name)
    if rows == []:
        #raise Exception("user not found")
        return None
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
    #FIXME: authentication should be:
    #       -search password by user name (join)  
    user = getUserByName(name)
    if user == None :
        return False
    
    saved = passwordQM.getPasswordByUserId(user.id)
    generated = hashlib.sha256(password).hexdigest()
    if saved == generated:
        return user
    else:
        return False
    
    
    
    
    
    
    
    
    