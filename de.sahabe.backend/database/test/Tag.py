'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
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
        self.name = self.tag.name
    
    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertTag(self.id, self.name)
        
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])

    
    """ DATA TYPE TESTS """
    
    def testInsertInvalidId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertTag,
                          self.id + "e",
                          self.name)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertTag ,
                         self.id[:-13], self.name, self.email)
        """
            
    def testInsertInvalidName(self):
        name = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertTag,
                          self.id,
                          name)
    

    """ NULL CONSTRAINS TESTS """    
        
    def testInsertNoId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "tag",
                          name=self.name)
    
     
    
    def testInsertNoName(self):
        self.assertRaisesRegexp(OperationalError, "Field 'name' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "tag",
                          id=self.id)

    
    """ UNIQUE CONSTRAINS TESTS """
    def testInsertDublicateId(self):
        self.insertTag(self.id, self.name)
        _id = self.id
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertTag,
                          _id,
                          self.name)
        
    def testInsertDublicateName(self):
        self.insertTag(self.id, self.name)
        name = self.name
        self.__initDependencies()
        self.insertTag(self.id,
                       name)

    #TODO: implement update entries tests
    #TODO: implement drop entries test