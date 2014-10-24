'''
Created on Jul 5, 2014

@author: abo
'''

from app.db import DBApiModule as db


class User():
    
    def __init__(self, resultSet):
        self.id = resultSet[0][0]
        self.username = resultSet[0][1]
        self.email = resultSet[0][2]
        
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
        db.insertToTable(conn, "table", id = self.id, name = self.username, email = self.email)
    
    def __repr__(self):
        return '<User %r>' % (self.id)