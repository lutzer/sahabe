'''
Created on Jun 13, 2014

@author: maan al balkhi
'''
import string
import random
import uuid as uid
import hashlib
import datetime


def randomName(size=32, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(random.randint(8, size)))

def randomEmail(size=32): 
    return randomText(size - 10) + "@sahabe.de"
    
def randomText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def uuid():
    return str(uid.uuid4())

def timeStamp():
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(timeStamp)


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
            self.id = uuid()
            self.name = randomName()
            self.email = self.name + "@sahabe.de"
    
    class Category():
        id = ""
        userId = ""
        name = ""
        def __init__(self, user):
            self.id = uuid()
            self.userId = user.id
            self.name = randomName()
    
    class Link():
        id = ""
        userId = ""
        catId = ""
        url = ""
        name = ""
        description = ""
        createDate = ""
        def __init__(self, user, category):
            self.id = uuid()
            self.userId = user.id
            self.catId = category.id
            self.url = randomText(64)
            self.name = randomName()
            self.desciption = randomText(36)
            """ make datetime stamp """
            self.createDate = timeStamp()
    
    class Tag():
        id = ""
        userId = ""
        name = ""
        groupTag = '0'
        def __init__(self, user):
            self.id = uuid()
            self.userId = user.id
            self.name = randomName()
            self.groupTag = '0'
    
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
            self.value = hashlib.sha256(randomText(16)).hexdigest()
            self.salt = randomText(64, string.ascii_lowercase + string.digits)
