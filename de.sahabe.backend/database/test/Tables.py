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
database="sahabe_test"

# FIXME: run initialize new tables 
#sdbinit.run(host, dbUser, dbPw, database)

class Tables(unittest.TestCase):
    
    def connect(self):
        self.conn = db.connect("localhost",
                               "sahabe_test",
                               "sahabe_test",
                               "sahabe_test")
        
    def initDBMockContents(self):
        entry = mock()
        self.user = entry.user
        self.cat = entry.category
        self.link = entry.link
        self.tag = entry.tag
        self.tagMap = entry.tagMap
        self.pw = entry.pw
    
    def insertUser(self, _id, name, email):
        db.insertToTable(self.conn, "user",
                         id=_id, name=name, email=email)
            
    def insertCategory(self, _id, userId, name):
        db.insertToTable(self.conn, "category",
                         id=_id, user_id=userId, name=name)
    
    def insertLink(self, _id, userId, catId, url, name, desc, createDate):
        db.insertToTable(self.conn, "link", id=_id, user_id=userId,
                         category_id=catId, url=url, name=name,
                         description=desc, create_date=createDate)
    
    def insertTag(self, _id, userId, name, gTag):
        db.insertToTable(self.conn, "tag", id=_id, user_id=userId,
                         name=name, group_tag=str(gTag))
    
    def insertTagMap(self, linkId, tagId):
        db.insertToTable(self.conn, "tag_map", link_id=linkId,
                         tag_id=tagId)
        
    def insertPW(self, userId, value, salt):
        db.insertToTable(self.conn, "pw_hash", user_id=userId,
                         value=value, salt=salt)
 
        
    def extractNumber(self, _str):    
        result = ""
        split = list(_str)
        for s in split:
            if s.isdigit():
                result += s
        return int(result)
    

    def setUp(self):
        self.connect()
        self.initDBMockContents()
        
    def tearDown(self):
        self.conn.close()

    def testMockReferences(self):
        self.assertEqual(self.user.id, self.link.userId)
        self.assertEqual(self.user.id, self.tag.userId)
        self.assertEqual(self.user.id, self.cat.userId)
        self.assertEqual(self.user.id, self.pw.userId)
        self.assertEqual(self.cat.id, self.link.catId)
        self.assertEqual(self.link.id, self.tagMap.linkId)
        self.assertEqual(self.tag.id, self.tagMap.tagId)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
