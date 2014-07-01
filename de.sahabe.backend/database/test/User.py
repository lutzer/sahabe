'''
Created on Jun 14, 2014

@author: Maan Al Balkhi
'''
import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class User(Tables.Tables):
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
        self.id = self.user.id
        self.name = self.user.name
        self.email = self.user.email
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertUser(self.id, self.name, self.email)
        
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(self.email, rows[0][2])

    
    """ DATA TYPE TESTS """
    
    def testInsertInvalidId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertUser,
                          self.id + "e",
                          self.name,
                          self.email)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertUser ,
                         self.id[:-13], self.name, self.email)
        """
        
    def testInsertInvalidName(self):
        name = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertUser,
                          self.id,
                          name,
                          self.email)
    
    def testInsertInvalidEmail(self):
        email = mock.randomEmail(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertUser,
                          self.id,
                          self.name,
                          email)


    
    """ NULL CONSTRAINS TESTS """    
        
    def testInsertNoId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "user",
                          name=self.name,
                          email=self.email)
        
    def testInsertNoName(self):
        self.assertRaisesRegexp(OperationalError, "Field 'name' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "user",
                          id=self.id,
                          email=self.email)
        
    def testInsertNoEmail(self):
        self.assertRaisesRegexp(OperationalError, "Field 'email' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "user",
                          id=self.id,
                          name=self.name)
        
    
    """ UNIQUE CONSTRAINS TESTS """
        
    def testInsertDublicateId(self):
        self.insertUser(self.id, self.name, self.email)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertUser,
                          self.id,
                          mock.randomName(),
                          mock.randomEmail())
        
    def testInsertDublicateName(self):
        self.insertUser(self.id, self.name, self.email)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertUser,
                          mock.uuid(),
                          self.name,
                          mock.randomEmail())
        
    def testInsertDublicateEmail(self):
        self.insertUser(self.id, self.name, self.email)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertUser,
                          mock.uuid(),
                          mock.randomName(),
                          self.email)
        
    #TODO: implement update entries tests
    #TODO: implement drop entries test
