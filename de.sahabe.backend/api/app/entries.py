'''
Created on Jul 5, 2014

@author: abo
'''

from impl import DBApiModule as db


def get_user_by_id(_id):
    conn = db.connect()
    rows = db.selectFrom(conn, {"user"}, "*", id = _id)
    return User(rows[0][0], rows[0][1], rows[0][2])
    
def get_user_by_name(name):
    conn = db.connect()
    rows = db.selectFrom(conn, {"user"}, "*", name = name)
    if rows == []:
        raise Exception("user not found")
    return User(rows[0][0], rows[0][1], rows[0][2])

def get_pw_hash_by_user_id(userId):
    conn = db.connect()
    rows = db.selectFrom(conn, {"pw_hash"}, "value", user_id = userId)
    return rows[0][0]

class User():
    
    def __init__(self, _id, name, email):
        self.id = _id
        self.nickname = name
        self.email = email
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def add_user(self):
        conn = db.connect()
        db.insertToTable(conn, "table", id = self.id, name = self.nickname, email = self.email)
    
    def __reper__(self):
        return '<User %r>' % (self.id)