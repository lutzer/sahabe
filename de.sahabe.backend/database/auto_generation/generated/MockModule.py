
import string
import random
import uuid as uid
import hashlib
import datetime


def randomText(size=64 , chars=string.ascii_letters + string.digits + string.punctuation):
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

def SHA2():
    return hashlib.sha256(randomText(16)).hexdigest()
    
def MD5():
    return hashlib.md5(randomText(16)).hexdigest()

class DBMock():

    def __init__(self):
        self.user = DBMock.User()
        self.link = DBMock.Link(self.user)
        self.searchTable = DBMock.SearchTable(self.user, self.link)
        self.tag = DBMock.Tag()
        self.linkTagMap = DBMock.LinkTagMap(self.tag, self.link)

    class User(object):
    
        def __init__(self):
            self.id = uuid()
            self.name = randomText(64)
            self.email = randomText(64)

    class Link(object):
    
        def __init__(self, user):
            self.id = uuid()
            self.userId = user.id
            self.url = randomText(2048)
            self.urlHash = MD5()
            self.title = randomText(256)
            self.description = randomText(256)
            self.typeName = randomText(64)
            self.modifiedAt = timeStamp()

    class SearchTable(object):
    
        def __init__(self, user, link):
            self.userId = user.id
            self.linkId = link.id
            self.groups = randomText(256)
            self.tags = randomText(256)
            self.text = randomText(2048)

    class Tag(object):
    
        def __init__(self):
            self.id = uuid()
            self.name = randomText(64)

    class LinkTagMap(object):
    
        def __init__(self, tag, link):
            self.tagId = tag.id
            self.linkId = link.id
