'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
'''

import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class PassWord(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    - Test: FOREIGN KEY Constrains
    """ 

    def __initDependencies(self):
        self.initDBMockContents()
        self.userId = self.pw.userId
        self.value = self.pw.value
        self.salt = self.pw.salt
        self.insertUser(self.user.id, self.user.name, self.user.email)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertPW(self.userId, self.value, self.salt)
        
        rows = db.selectFrom(self.conn, "pw_hash", "*", user_id=self.userId)
        
        self.assertEqual(self.user.id, rows[0][0])
        self.assertEqual(self.value, rows[0][1])
        self.assertEqual(self.salt, rows[0][2])
    
    """ DATA TYPE TESTS """
    
    def testInsertInvalidUserId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertPW,
                          self.userId + "e",
                          self.value,
                          self.salt)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertTag ,
                         self.id[:-13], self.name, self.email)
        """
            
    def testInsertInvalidValue(self):
        value = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertPW,
                          self.userId,
                          value,
                          self.salt)
        
    def testInsertInvalidSalt(self):
        salt = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertPW,
                          self.userId,
                          self.value,
                          salt)


    """ NULL CONSTRAINS TESTS """    
        
    def testInsertNoUserId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'user_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "pw_hash",
                          value=self.value,
                          salt=self.salt)
    
    def testInsertNoName(self):
        self.assertRaisesRegexp(OperationalError, "Field 'value' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "pw_hash",
                          user_id=self.userId,
                          salt=self.salt)
        
    def testInsertNoSalt(self):
        self.assertRaisesRegexp(OperationalError, "Field 'salt' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "pw_hash",
                          user_id=self.userId,
                          value=self.value)
    
    
    """ UNIQUE CONSTRAINS TESTS """
    def testInsertDublicateUserId(self):
        self.insertPW(self.userId, self.value, self.salt)
        userId = self.userId
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertPW,
                          userId,
                          self.value,
                          self.salt)
        
    def testInsertDublicateValue(self):
        self.insertPW(self.userId, self.value, self.salt)
        value = self.value
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertPW,
                          self.userId,
                          value,
                          self.salt)
        
    def testInsertDublicateSalt(self):
        self.insertPW(self.userId, self.value, self.salt)
        salt = self.salt
        self.__initDependencies()
        self.insertPW(self.userId,
                      self.value,
                      salt)
        
    
    """ FOREIGN KEY CONSTRAINS TESTS """
    def testInsertNotExistingUserId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertPW,
                          mock.uuid(),
                          self.value,
                          self.salt)
        
    #TODO: implement update user.id tests
    #TODO: implement drop user.id test
    
    