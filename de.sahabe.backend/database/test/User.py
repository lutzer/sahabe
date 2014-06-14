'''
Created on Jun 14, 2014

@author: maan al balkhi
'''
from _mysql import DataError, IntegrityError
from _mysql_exceptions import OperationalError
from impl.DBApiModule import DataTypes as dt
import Tables as tb
import impl.DBApiModule as db
import test.MockModule as mock


class TestTablesInsertion(tb.unittest.TestCase):
                    
    def setUp(self):
        self.conn = tb.connect()
        user = tb.mock().user
        self.id = user.id
        self.name = user.name
        self.email = user.email
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        tb.insertUser(self.conn, self.id, self.name, self.email)
        
        rows = db.selectFrom(self.conn, "user", "id", "name", "email", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(self.email, rows[0][2])
    
    def testInsertInvalidId(self):
        """ too long """
        self.assertRaises(DataError, tb.insertUser , self.conn,
                         self.id + "e", self.name, self.email)
        """ too short """
        """
        self.assertRaises(DataError, tb.insertUser ,self.conn,
                         self.id[:-2], self.name, self.email)
        """
    def testInsertInvalidName(self):
        name = mock.generateText(tb.extractNumber(dt.VCHAR64) + 2)
        self.assertRaises(DataError, tb.insertUser , self.conn,
                         self.id , name, self.email)
    
    def testInsertInvalidEmail(self):
        email = mock.generateEmail(tb.extractNumber(dt.VCHAR64) + 2)
        self.assertRaises(DataError, tb.insertUser , self.conn,
                         self.id , self.name, email)
        
    def testInsertNoId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn,
                         "user", name=self.name, email=self.email)
        
    def testInsertNoName(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn,
                         "user", id=self.id, email=self.email)
    def testInsertNoEmail(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn,
                         "user", id=self.id, name=self.name)
        
    def testInsertDublicateId(self):
        tb.insertUser(self.conn, self.id, self.name, self.email)
        self.assertRaises(IntegrityError, tb.insertUser, self.conn, self.id,
                          mock.generateName(), mock.generateEmail())
        
    def testInsertDublicateName(self):
        tb.insertUser(self.conn, self.id, self.name, self.email)
        self.assertRaises(IntegrityError, tb.insertUser, self.conn,
                          str(mock.uuid.uuid4()), self.name, mock.generateEmail())
        
    def testInsertDublicateEmail(self):
        tb.insertUser(self.conn, self.id, self.name, self.email)
        self.assertRaises(IntegrityError, tb.insertUser, self.conn,
                          str(mock.uuid.uuid4()), mock.generateName(), self.email)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    tb.unittest.main()
