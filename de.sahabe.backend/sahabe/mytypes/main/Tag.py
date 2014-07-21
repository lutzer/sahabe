'''
Created on Jul 21, 2014

@author: Maan Al Balkhi
'''

from common.main import utils

class Tag():
   
    def __init__(self, _id, userId, name):
        self.id = _id
        self.userId = userId
        self.name = name
   
   
    @staticmethod
    def newTag(userId, name):
        return Tag(utils.uuid(),
                   userId,
                   name)
   
    @staticmethod
    def fromResultRecord(resultRecord):
        return Tag(resultRecord[0],
                   resultRecord[1],
                   resultRecord[2])
    
    
    def __repr__(self):
        return '<Tag %r>' % (self.name)