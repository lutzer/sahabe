'''
Created on Jun 13, 2014

@author: maan al balkhi
'''
import unittest
import impl.DBApiModule as db
import impl.InitSahabeDB as dbinit
from test.MockModule import DBMock as mock

host = "localhost"
dbUser = "sahabe_test"
dbPw = "sahabe_test"
database = "sahabe_test"

def connect():
    return db.connect(host, dbUser, dbPw, database)

def init():
    dbinit.run(host, dbUser, dbPw, database)
    
def insertUser(conn, _id, _name, _email):
    db.insertToTable(conn, "user", id=_id,
                     name=_name, email=_email)
    
def insertCategory(self):
    db.insertToTable(self.conn, "category",
                     id=self.cat.id, user_id=self.cat.userId, name=self.cat.name)

def insertLink(self):
    db.insertToTable(self.conn, "link", id=self.link.id, user_id=self.link.userId,
                     category_id=self.link.categoryId, url=self.link.url,
                     name=self.link.name, description=self.link.description,
                     create_date=self.link.createDate)

def insertTag(self):
    db.insertToTable(self.conn, "tag", id=self.tag.id, user_id=self.tag.userId,
                     name=self.tag.name, group_tag=str(self.tag.groupTag))

def insertTagMap(self):
    db.insertToTable(self.conn, "tag_map",link_id=self.tagMap.linkId,
                    tag_id=self.tagMap.tagId)
    
def __insertPW(self):
        db.insertToTable(self.conn, "pw_hash", user_id=self.pw.userId,
                         value=self.pw.value, salt=self.pw.salt)    
    
def extractNumber(_str):    
    result=""
    split = list(_str)
    for s in split:
        if s.isdigit():
            result+=s
    return int(result)

class TestTablesInsertion(unittest.TestCase):
   
    def setUp(self):
        self.conn = db.connect(host, dbUser, dbPw , database)
        entry = mock()
        self.user = entry.user
        self.cat = entry.category
        self.link = entry.link
        self.tag = entry.tag
        self.tagMap = entry.tagMap
        self.pw = entry.pw   
        
    def tearDown(self):
        self.conn.close()

    def testMockReferences(self):
        self.assertEqual(self.user.id, self.link.userId)
        self.assertEqual(self.user.id, self.tag.userId)
        self.assertEqual(self.user.id, self.cat.userId)
        self.assertEqual(self.user.id, self.pw.userId)
        self.assertEqual(self.cat.id, self.link.categoryId)
        self.assertEqual(self.link.id, self.tagMap.linkId)
        self.assertEqual(self.tag.id, self.tagMap.tagId)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
