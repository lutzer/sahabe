'''
Created on Jun 15, 2014

@author: maan al balkhi
'''
import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError

class Category(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    """
    

    def setUp(self):
        self.connect()
        self.initDBMockContents()
        self.id = self.cat.id
        self.userId = self.cat.userId
        self.name = self.cat.name
        self.insertUser(self.user.id, self.user.name, self.user.email)

    def tearDown(self):
        self.conn.close()


    def testInsertion(self):
        self.insertCategory(self.id, self.userId, self.name)
        rows = db.selectFrom(self.conn, "category", "id", "user_id", "name", id=self.id)

        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.name, rows[0][2])

    def testInsertInvalidId(self):
        self.assertRaises(DataError, self.insertCategory,
                         self.id + "e", self.userId, self.name)
        # FIXME: what's about UUID ??? 
        """
        self.assertRaises(DataError, self.insertUser ,
                         self.id[:-13], self.name, self.email)
        """
        
    def testInsertInvalidUserId(self):
        self.assertRaises(DataError, self.insertCategory,
                         self.id , self.userId + "e", self.name)
        
    def testInsertInvalidName(self):
        name = mock.generateText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaises(DataError, self.insertCategory,
                         self.id , self.userId , name)
        
    def testInsertNoId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn,
                         "category", user_id=self.userId, name=self.name)
        
    def testInsertNoUserId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn,
                         "category", id=self.id, name=self.name)
        
    def testInsertNoName(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn,
                         "category", id=self.id, user_id=self.userId)
        
    # FIXME: what's about UNIQUE constrains. 
        
    def testInsertDoublicateId(self):
        self.insertCategory(self.id, self.userId, self.name)
        self.assertRaises(IntegrityError, self.insertCategory, self.id,
                          mock.uuid(), mock.generateName())
        
    def testInsertDoublicateUserId(self):
        self.insertCategory(self.id, self.userId, self.name)
        self.assertRaises(IntegrityError, self.insertCategory,
                          mock.uuid(), self.userId, mock.generateName())
        
    def testInsertDoublicateName(self):
        self.insertCategory(self.id, self.userId, self.name)
        self.assertRaises(IntegrityError, self.insertCategory,
                          mock.uuid(), mock.uuid(), self.name)
