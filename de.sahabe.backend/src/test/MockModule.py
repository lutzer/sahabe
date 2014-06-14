'''
Created on Jun 13, 2014

@author: maan al balkhi
'''
import string
import random
import uuid
import hashlib
import time
import datetime

def generateName(size=32, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(random.randint(2, size)))

def generateEmail(size=32): 
    return generateText(size-10)+"@sahabe.de"
    
def generateText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class DBMock():
    """
    user, category, tag, link, tag_map, pw_hash 
    """
    user = ""
    category = ""
    tag = ""
    link = ""
    tagMap = ""
    pw = ""
    
    def __init__(self):
        self.user = DBMock.User()
        self.category = DBMock.Category(self.user)
        self.tag = DBMock.Tag(self.user)
        self.link = DBMock.Link(self.user, self.category)
        self.tagMap = DBMock.TagMap(self.link, self.tag)
        self.pw = DBMock.PWHash(self.user)
    
    class User(object):
        id = ""
        name = ""
        email = ""
    
        def __init__(self):
            self.id = str(uuid.uuid4())
            self.name = generateName()
            self.email = self.name + "@sahabe.de"
    
    class Category():
        id = ""
        userId = ""
        name = ""
        def __init__(self, user):
            self.id = str(uuid.uuid4())
            self.userId = user.id
            self.name = generateName()
    
    class Link():
        id = ""
        userId = ""
        categoryId = ""
        url = ""
        name = ""
        description = ""
        createDate = ""
        
        def __init__(self, user, category):
            self.id = str(uuid.uuid4())
            self.userId = user.id
            self.categoryId = category.id
            self.url = generateText(64)
            self.name = generateName()
            self.desciption = generateText(36)
            """ make datetime stamp """
            self.createDate = str(datetime.datetime.fromtimestamp(time.time()))
    
    class Tag():
        id = ""
        userId = ""
        name = ""
        groupTag = 0
        def __init__(self, user):
            self.id = str(uuid.uuid4())
            self.userId = user.id
            self.name = generateName()
            self.groupTag = 0
    
    class TagMap():
        linkId = ""
        tagId = ""
        
        def __init__(self, link, tag):
            self.linkId = link.id
            self.tagId = tag.id
    
    class PWHash():
        userId = "" 
        value = ""
        salt = ""
        
        def __init__(self, user):
            self.userId = user.id 
            self.value = hashlib.sha256(generateText(16)).hexdigest()
            self.salt = generateText(64, string.ascii_lowercase + string.digits)
