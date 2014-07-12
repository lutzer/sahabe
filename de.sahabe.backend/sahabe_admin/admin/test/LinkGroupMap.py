'''
Created on Jun 27, 2014

@author: Maan Al Balkhi
'''

import Tables
import admin.main.MockModule as mock
import admin.main.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class LinkGroupMap(Tables.Tables):
    '''
    - Test: insertion and fetching data from/to table
    - Test: update entry and its references
    - Test: drop entry and its references
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    - Test: FOREIGN KEY CONSTRAINS
    ''' 
    
    def __initDependencies(self):
        self.initDBMockContents()
        self.groupId = self.linkGroupMap.groupId
        self.linkId = self.linkGroupMap.linkId
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertGroup(self.group.id, self.group.name, self.group.public)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.urlHash,
                        self.link.title, self.link.description, self.link.typeName, self.link.modifiedAt)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
        
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        
        rows = db.selectFrom(self.conn, {"link_group_map"}, "*", group_id=self.groupId, link_id=self.linkId)
        
        self.assertEqual(self.group.id, rows[0][0])
        self.assertEqual(self.link.id, rows[0][1])
    
    
    ''' UPDATE TESTS '''
        
    def testUpdateToExistingGroupId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        linkGroupMap = self.linkGroupMap
        self.__initDependencies()
        db.updateInTable(self.conn,
                         {"group_id":self.groupId},
                         "link_group_map",
                         group_id=linkGroupMap.groupId)
        rows = db.selectFrom(self.conn, {"link_group_map"}, "*", group_id=self.groupId)
        
        self.assertEqual(self.groupId, rows[0][0])
        self.assertEqual(linkGroupMap.linkId, rows[0][1])
     
    def testUpdateToExistingLinkId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        linkGroupMap = self.linkGroupMap
        self.__initDependencies()
        db.updateInTable(self.conn,
                         {"link_id":self.linkId},
                         "link_group_map",
                         link_id=linkGroupMap.linkId)
        rows = db.selectFrom(self.conn, {"link_group_map"}, "*", link_id=self.linkId)
        
        self.assertEqual(linkGroupMap.groupId, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])   
    
    def testUpdateToNonExistingGroupId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        groupId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"group_id":groupId},
                                "link_group_map",
                                group_id=self.groupId)

    def testUpdateToNonExistingLinkId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        linkId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"link_id":linkId},
                                "link_group_map",
                                link_id=self.linkId)    
            
    
    ''' DROP TESTS '''
        
    def testLinkGroupMap(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        db.deleteFromTable(self.conn, "link_group_map", group_id=self.groupId)
        rows = db.selectFrom(self.conn, {"link_group_map"}, "*", group_id=self.groupId)
        self.assertEquals(rows, [])
    
    
    ''' DATA TYPE TESTS '''
    
    def testInsertInvalidGroupId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLinkGroupMap,
                          self.groupId + "e",
                          self.linkId)
        ''' insert too short '''
        # FIXME: what's about UUID length constrains? 
        '''
        self.assertRaises(DataError, self.insertgroup ,
                         self.id[:-13], self.name, self.email)
        '''
            
    def testInsertInvalidLinkId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLinkGroupMap,
                          self.groupId,
                          self.linkId + "e")
        ''' insert too short '''
        # FIXME: what's about UUID length constrains? 
        '''
        self.assertRaises(DataError, self.insertgroup ,
                         self.id[:-13], self.name, self.email)
        '''

    ''' NULL CONSTRAINS TESTS '''    
        
    def testInsertNogroupId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'group_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_group_map",
                          link_id=self.linkId)
    
     
    
    def testInsertNoLinkId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'link_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_group_map",
                          group_id=self.groupId)

    
    ''' UNIQUE CONSTRAINS TESTS '''
    def testInsertDublicategroupId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        groupId = self.groupId
        self.__initDependencies()
        self.insertLinkGroupMap(groupId,
                       self.linkId)
        
    def testInsertDublicateLinkId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        linkId = self.linkId
        self.__initDependencies()
        self.insertLinkGroupMap(self.groupId,
                       linkId)
        
    def testInsertDublicategroupAndLinkId(self):
        self.insertLinkGroupMap(self.groupId, self.linkId)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertLinkGroupMap,
                          self.groupId,
                          self.linkId)
    
    
    ''' FOREIGN KEY CONSTRAINS TESTS '''
    
    def testInsertNonExistinggroupId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertLinkGroupMap,
                                mock.uuid(),
                                self.linkId)
        
    def testInsertNonExistingLinkId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertLinkGroupMap,
                                self.groupId,
                                mock.uuid())
