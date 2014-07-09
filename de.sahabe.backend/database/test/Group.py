'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
'''

import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class Group(Tables.Tables):
    '''
    - Test: insertion and fetching data from/to table
    - Test: update entry and its references
    - Test: drop entry and its references
    - Test: references
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    ''' 

    def __initDependencies(self):
        self.initDBMockContents()
        self.id = self.group.id
        self.name = self.group.name
        self.public = self.group.public
    
    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
    
    
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertGroup(self.id, self.name, self.public)
        
        rows = db.selectFrom(self.conn, {"link_group"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(int(self.public), rows[0][2])
        
    
    ''' UPDATE TESTS '''
        
    def testUpdateId(self):
        self.insertGroup(self.id, self.name, self.public)
        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "link_group", id=self.id)
        
        rows = db.selectFrom(self.conn, {"link_group"}, "*", id=_id)
        
        self.assertEqual(_id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(int(self.public), rows[0][2])
        
    def testUpdateName(self):
        self.insertGroup(self.id, self.name, self.public)
        name = mock.randomName()
        db.updateInTable(self.conn, {"name":name}, "link_group", id=self.id)
        
        rows = db.selectFrom(self.conn, {"link_group"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(name, rows[0][1])
        self.assertEqual(int(self.public), rows[0][2])
        
    def testUpdatePublic(self):
        self.insertGroup(self.id, self.name, self.public)
        db.updateInTable(self.conn, {"public":"1"}, "link_group", id=self.id)
        
        rows = db.selectFrom(self.conn, {"link_group"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(1, rows[0][2])
        
    def testUpdateIdReferencedToLinkGroupMap(self):
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertGroup(self.id, self.name, self.public)
        self.insertLinkGroupMap(self.linkGroupMap.groupId, self.linkGroupMap.linkId)
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "link_group",
                                id=self.id)

        
    ''' DROP TESTS '''
        
    def testDropGroup(self):
        self.insertGroup(self.id, self.name, self.public)
        db.deleteFromTable(self.conn, "link_group", id=self.id)
        rows = db.selectFrom(self.conn, {"link_group"}, "*", id=self.id)
        self.assertEquals(rows, [])
        
    def testDropLinkGroupMapByGroup(self):
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.title,
                        self.link.description, self.link.typeName , self.link.modifiedAt)
        self.insertGroup(self.id, self.name, self.public)
        self.insertLinkGroupMap(self.linkGroupMap.groupId, self.linkGroupMap.linkId)
        
        db.deleteFromTable(self.conn, "link_group", id=self.id)
        row = db.selectFrom(self.conn, {"link_group_map"}, "*", group_id=self.id)
        self.assertEqual(row, [])
        
    
    ''' DATA TYPE TESTS '''
    
    def testInsertInvalidId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertGroup,
                          self.id + "e",
                          self.name,
                          self.public)
        ''' insert too short '''
        # FIXME: what's about UUID length constrains? 
        '''
        self.assertRaises(DataError, self.insertTag ,
                         self.id[:-13], self.name, self.email)
        '''
            
    def testInsertInvalidName(self):
        name = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertGroup,
                          self.id,
                          name,
                          self.public)
        
    def testInsertInvalidPublic_char(self):
        self.assertRaises(OperationalError, self.insertGroup,
                          self.id,
                          self.name,
                          'e')
        self.assertRaises(OperationalError, self.insertGroup,
                          self.id,
                          self.name,
                          'e' + self.public)
        self.assertRaises(OperationalError, self.insertGroup,
                          self.id,
                          self.name,
                          self.public + 'e')

    def testInsertInvalidPublic_bigNum(self):
        self.insertGroup(self.id,
                         self.name,
                         "25")


    ''' NULL CONSTRAINS TESTS '''    
        
    def testInsertNoId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_group",
                          name=self.name,
                          public=self.public)
    
    def testInsertNoName(self):
        self.assertRaisesRegexp(OperationalError, "Field 'name' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_group",
                          id=self.id,
                          public=self.public)
        
    def testInsertNoPublic(self):
        self.assertRaisesRegexp(OperationalError, "Field 'public' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_group",
                         id=self.id,
                         name=self.name)
    
    
    ''' UNIQUE CONSTRAINS TESTS '''
    def testInsertDublicateId(self):
        self.insertGroup(self.id, self.name, self.public)
        _id = self.id
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertGroup,
                          _id,
                          self.name,
                          self.public)
        
    def testInsertDublicateName(self):
        self.insertGroup(self.id, self.name, self.public)
        name = self.name
        self.__initDependencies()
        self.insertGroup(self.id,
                         name,
                         self.public)
        
    def testInsertDublicateSalt(self):
        self.insertGroup(self.id, self.name, self.public)
        public = self.public
        self.__initDependencies()
        self.insertGroup(self.id,
                         self.name,
                         public)
