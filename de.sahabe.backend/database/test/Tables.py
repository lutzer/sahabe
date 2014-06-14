'''
Created on Jun 13, 2014

@author: maan al balkhi
'''
import unittest
import impl.DBApiModule as db
import impl.InitSahabeDB as init   
from test.MockModule import DBMock as mock
from _mysql_exceptions import IntegrityError

host = "localhost"
dbUser = "sahabe_test"
dbPw = "sahabe_test"
database = "sahabe_test"

init.run(host, dbUser, dbPw, database)

class TestTablesInsertion(unittest.TestCase):
    entry = None
    conn = None

    def setUp(self):
        self.entry = mock()
        self.conn = db.connect(host, dbUser, dbPw , database)
        
        
    def tearDown(self):
        self.conn.close()

    def testMockReferences(self):
        self.assertEqual(self.entry.user.id, self.entry.link.userId)
        self.assertEqual(self.entry.user.id, self.entry.tag.userId)
        self.assertEqual(self.entry.user.id, self.entry.category.userId)
        self.assertEqual(self.entry.user.id, self.entry.pw.userId)
        self.assertEqual(self.entry.category.id, self.entry.link.categoryId)
        self.assertEqual(self.entry.link.id, self.entry.tagMap.linkId)
        self.assertEqual(self.entry.tag.id, self.entry.tagMap.tagId)
    
    def testInsertToUser(self):
        user = self.entry.user
        db.insertToTable(self.conn, "user", "id", "name", "email",
                         id=user.id, name=user.name, email=user.email)    
        rows = db.selectFrom(self.conn, "user", "id", "name", "email", id=user.id)
        
        self.assertEqual(user.id, rows[0][0])
        self.assertEqual(user.name, rows[0][1])
        self.assertEqual(user.email, rows[0][2])
        
    
    
    def testInsertDoublicateToUser(self):
        user = self.entry.user
        
        db.insertToTable(self.conn, "user", "id", "name", "email",
                         id=user.id, name=user.name, email=user.email)
        
        self.assertRaises(IntegrityError,db.insertToTable, self.conn,"user", "id", "name", "email",
                         id=user.id, name=user.name, email=user.email)
    
    
    
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
