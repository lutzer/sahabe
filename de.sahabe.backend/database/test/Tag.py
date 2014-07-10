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
    - Test: update entry and its references
    - Test: drop entry and its references
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
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertTag(self.id, self.name)
        
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        
        
    ''' UPDATE TESTS '''
        
    def testUpdateId(self):
        self.insertTag(self.id, self.name)
        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "tag", id=self.id)
        
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=_id)
        
        self.assertEqual(_id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        
    def testUpdateName(self):
        self.insertTag(self.id, self.name)
        name = mock.randomText()
        db.updateInTable(self.conn, {"name":name}, "tag", id=self.id)
        
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(name, rows[0][1])
        
    def testUpdateTagIdReferenceToLinkTagMap(self):
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertTag(self.id, self.name)
        self.insertLinkTagMap(self.linkTagMap.tagId, self.linkTagMap.linkId)
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "tag",
                                id=self.id)
        
    ''' DROP TESTS '''
        
    def testDropTag(self):
        self.insertTag(self.id, self.name)
        db.deleteFromTable(self.conn, "tag", id=self.id)
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)
        self.assertEquals(rows, [])
        
    def testDropLinkTagMapByTag(self):
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.title,
                        self.link.description, self.link.typeName , self.link.modifiedAt)
        self.insertTag(self.id, self.name)
        self.insertLinkTagMap(self.linkTagMap.tagId, self.linkTagMap.linkId)
        
        db.deleteFromTable(self.conn, "tag", id=self.id)
        row = db.selectFrom(self.conn, {"link_tag_map"}, "*", tag_id=self.id)
        self.assertEqual(row, [])
        
    
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
        name = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
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
