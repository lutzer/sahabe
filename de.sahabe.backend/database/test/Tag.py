'''
Created on Jun 15, 2014

@author: maan al balkhi
'''

'''
Created on Jun 14, 2014

@author: maan al balkhi
'''
import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class Tag(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    """ 
    
    def __initDependencies(self):
        self.initDBMockContents()
        self.id = self.tag.id
        self.userId = self.tag.userId
        self.name = self.tag.name
        self.groupTag = self.tag.groupTag
        self.insertUser(self.user.id, self.user.name, self.user.email)
    
    def setUp(self):
        self.connect()
        self.initDBMockContents()
        self.id = self.tag.id
        self.userId = self.tag.userId
        self.name = self.tag.name
        self.groupTag = self.tag.groupTag
        self.insertUser(self.user.id, self.user.name, self.user.email)
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertTag(self.id, self.userId, self.name, self.groupTag)
        
        rows = db.selectFrom(self.conn, "tag", "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.userId, rows[0][1])
        self.assertEqual(self.name, rows[0][2])
        self.assertEqual(self.groupTag, str(rows[0][3]))

    
    """ DATA TYPE TESTS """
    
    def testInsertInvalidId(self):
        self.assertRaises(DataError, self.insertTag,
                          self.id + "e",
                          self.userId,
                          self.name,
                          self.groupTag)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertTag ,
                         self.id[:-13], self.name, self.email)
        """
        
    def testInsertInvalidUserId(self):
        self.assertRaises(DataError, self.insertTag,
                          self.id,
                          self.userId + "e",
                          self.name,
                          self.groupTag)
            
    def testInsertInvalidName(self):
        name = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaises(DataError, self.insertTag,
                          self.id,
                          self.userId,
                          name,
                          self.groupTag)
    
    def testInsertInvalidGroubTag_char(self):
        #FIXME: for TINYINT every short number that's greater than 0 has the value true  
        self.assertRaises(OperationalError, self.insertTag,
                          self.id,
                          self.userId,
                          self.name,
                          "e" + self.groupTag)
        
        self.assertRaises(OperationalError, self.insertTag,
                          self.id,
                          self.userId,
                          self.name,
                          self.groupTag + "e")

        def testInsertInvalidGroubTag_bigNum(self):
            #FIXME: for TINYINT every short number that's greater than 0 has the value true  
            self.assertRaises(DataError, self.insertTag,
                              self.id,
                              self.userId,
                              self.name,
                              self.groupTag+"25")
    
    """ NULL CONSTRAINS TESTS """    
        
    def testInsertNoId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "tag",
                          user_id=self.userId,
                          name=self.name,
                          groub_tag=self.groupTag)
    
    def testInsertNoUserId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "tag",
                          id=self.id,
                          name=self.name,
                          groub_tag=self.groupTag)   
    
    def testInsertNoName(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "tag",
                          id=self.id,
                          user_id=self.userId,
                          groub_tag=self.groupTag)
        
    def testInsertNoGroupTag(self):
        db.insertToTable(self.conn, "tag",
                        id=self.id,
                        user_id=self.userId,
                        name=self.name)
        
    
    """ UNIQUE CONSTRAINS TESTS """
    # FIXME: what's about UNIQUE constrains?
    def testInsertDublicateId(self):
        self.insertTag(self.id, self.userId, self.name, self.groupTag)
        _id = self.id
        self.__initDependencies()
        self.assertRaises(IntegrityError, self.insertTag,
                          _id,
                          self.userId,
                          self.name,
                          self.groupTag)
        
    def testInsertDublicateUserId(self):
        self.insertTag(self.id, self.userId, self.name, self.groupTag)
        userId = self.userId
        self.__initDependencies()
        self.assertRaises(IntegrityError, self.insertTag,
                          self.id,
                          userId,
                          self.name,
                          self.groupTag)
        
    def testInsertDublicateName(self):
        self.insertTag(self.id, self.userId, self.name, self.groupTag)
        name = self.name
        self.__initDependencies()
        self.insertTag(self.id,
                       self.userId,
                       name,
                       self.groupTag)
                
    def testInsertDublicateGroupTag(self):
        self.insertTag(self.id, self.userId, self.name, self.groupTag)
        groupTag = self.groupTag
        self.__initDependencies()
        self.insertTag(self.id,
                       self.userId,
                       self.name,
                       groupTag)
        
   
        
        
        
        
        
        


