'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''
import uuid as uid

class Link():
    
    def __init__(self, resultSet):
        self.id = resultSet[0][0]
        self.userId = resultSet[0][1]
        self.url = resultSet[0][2]
        self.title = resultSet[0][3]
        self.description = resultSet[0][4]
        self.typeName = resultSet[0][5]
        self.modifiedAt = resultSet[0][6]
        
    def __repr__(self):
        return '<Link %r>' % (self.id)