'''
Created on Jun 13, 2014

@author: Maan Al Balkhi
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
# dbinit.run(host, dbUser, dbPw, database)

class Tables(unittest.TestCase):
    
    def connect(self):
        self.conn = db.connect("localhost",
                               "sahabe_test",
                               "sahabe_test",
                               "sahabe_test")
        
    def initDBMockContents(self):
        entry = mock()
        self.user = entry.user
        self.link = entry.link
        self.searchTable = entry.searchTable
        self.tag = entry.tag
        self.linkTagMap = entry.linkTagMap
        self.group = entry.group
        self.linkGroupMap = entry.linkGroupMap
        self.metaData = entry.metaData
        self.pw = entry.pw
    
    def insertUser(self, _id, name, email):
        db.insertToTable(self.conn, "user",
                         id=_id, name=name, email=email)
            
    def insertLink(self, _id, userId, url, urlHash, title, desc, typeName, modifiedAt):
        db.insertToTable(self.conn, "link", id=_id, user_id=userId, url=url, url_hash=urlHash,
                         title=title, description=desc, type_name=typeName, modified_at=modifiedAt)
    
    def insertSearchTable(self, userId, linkId, groups, tags, text):
        db.insertToTable(self.conn, "search_table",
                         user_id=userId, link_id=linkId, groups=groups, tags=tags, text=text)
    
    def insertTag(self, _id, name):
        db.insertToTable(self.conn, "tag", id=_id, name=name)
    
    def insertLinkTagMap(self, tagId, linkId):
        db.insertToTable(self.conn, "link_tag_map", tag_id=tagId,
                         link_id=linkId)
        
    def insertGroup(self, _id, name, public):
        db.insertToTable(self.conn, "link_group", id=_id, name=name, public=str(public))
    
    def insertLinkGroupMap(self, groupId, linkId):
        db.insertToTable(self.conn, "link_group_map", group_id=groupId,
                         link_id=linkId)
    
    def insertMetaData(self, linkId, key, value):
        db.insertToTable(self.conn, "meta_data",link_id=linkId, l_key=key, value=value)
        
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
        self.assertEqual(self.link.userId, self.user.id)
        self.assertEqual(self.searchTable.userId, self.user.id)
        self.assertEqual(self.searchTable.linkId, self.link.id)
        self.assertEqual(self.linkTagMap.tagId, self.tag.id)
        self.assertEqual(self.linkTagMap.linkId, self.link.id)
        self.assertEqual(self.linkGroupMap.groupId, self.group.id)
        self.assertEqual(self.linkGroupMap.linkId, self.link.id)
        self.assertEqual(self.metaData.linkId, self.link.id)
        self.assertEqual(self.pw.userId, self.user.id)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
