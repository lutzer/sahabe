'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

from app.common import utils

class Link():
    
    def __init__(self, _id, userId, url, title, description, typeName, modifiedAt):
        self.id = _id
        self.userId = userId
        self.url = url
        self.title = title
        self.description = description
        self.typeName = typeName
        self.modifiedAt = modifiedAt
        
        
    @staticmethod
    def newLink(userId, url, title, description, typeName, modifiedAt):
        return Link(utils.uuid(),
                    userId,
                    url,
                    title,
                    description,
                    typeName,
                    modifiedAt) 
    
    @staticmethod
    def fromResultRecord(resultRecord): 
        return Link(resultRecord[0],
                    resultRecord[1],
                    resultRecord[2],
                    resultRecord[4],
                    resultRecord[5],
                    resultRecord[6],
                    resultRecord[7])

    
    def __repr__(self):
        return '<Link %r>' % (self.id)