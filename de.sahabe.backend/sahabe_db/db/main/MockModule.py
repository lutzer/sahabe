'''
Created on Jun 13, 2014

@author: Maan Al Balkhi
'''
import string
import random
import uuid as uid
import hashlib
import datetime


def randomText(size=64 , chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(random.randint(5, size)))

def randomEmail(size=64): 
    return randomText(size - 10) + "@sahabe.de"
    
def randomFixedLengthText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def uuid():
    return str(uid.uuid4())

def timeStamp():
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(timeStamp)

class DBMock():
    """
    user, link, search_table, tag, link_tag_map, link_group, link_group_map, meta_data, pw_hash
    """
    user = ""
    link = ""
    searchTable = ""
    tag = ""
    linkTagMap = ""
    group = ""
    linkGroupMap =""
    metaData = ""
    pw = ""
    
    def __init__(self):
        self.user = DBMock.User()
        self.link = DBMock.Link(self.user)
        self.searchTable = DBMock.SearchTable(self.user, self.link)
        self.tag = DBMock.Tag()
        self.linkTagMap = DBMock.LinkTagMap(self.tag, self.link)
        self.group = DBMock.Group()
        self.linkGroupMap = DBMock.LinkGroupMap(self.group, self.link)
        self.metaData = DBMock.MetaData(self.link)
        self.pw = DBMock.PWHash(self.user)
    
    class User(object):
        id = ""
        name = ""
        email = ""
        def __init__(self):
            self.id = uuid()
            self.name = randomText()
            self.email = randomEmail()
    
    class Link():
        id = ""
        userId = ""
        url = ""
        title = ""
        description = ""
        typeName = ""
        modifiedAt = ""
        def __init__(self, user):
            self.id = uuid()
            self.userId = user.id
            self.url = randomText(2048)
            self.urlHash = hashlib.md5(self.url).hexdigest()
            self.title = randomText()
            self.desciption = randomText()
            self.typeName = randomText()
            self.modifiedAt = timeStamp()
            
    class SearchTable():
        userId = ""
        linkId = ""
        groups = ""
        tags = ""
        text = ""
        def __init__(self, user, link):
            self.userId = user.id
            self.linkId = link.id
            self.groups = randomText()
            self.tags = randomText()
            self.text = randomText()
            
    class Tag():
        id = ""
        name = ""
        def __init__(self):
            self.id = uuid()
            self.name = randomText()
    
    class LinkTagMap():
        tagId = ""
        linkId = ""
        def __init__(self, tag, link):
            self.tagId = tag.id
            self.linkId = link.id
            
    class Group():
        id = ""
        name = ""
        public = "0"
        def __init__(self):
            self.id = uuid()
            self.name = randomText()      
            self.public = "0"
            
    class LinkGroupMap():
        groupId = ""
        linkId = ""
        def __init__(self, group, link):
            self.groupId = group.id
            self.linkId = link.id
            
    class MetaData():
        linkId = ""
        key = ""
        value = ""       
        def __init__(self, link):   
            self.linkId = link.id
            self.key = randomText()
            self.value = randomText()
    
    class PWHash():
        userId = "" 
        value = ""
        salt = ""
        def __init__(self, user):
            self.userId = user.id 
            self.value = hashlib.sha256(randomText(16)).hexdigest()
            self.salt = randomText(64, string.ascii_lowercase + string.digits)
