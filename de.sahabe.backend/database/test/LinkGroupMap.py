'''
Created on Jun 27, 2014

@author: Maan Al Balkhi
'''

import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class LinkGroupMap(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    - Test: FOREIGN KEY CONSTRAINS
    """ 
    
    def __initDependencies(self):
        self.initDBMockContents()
        self.groupId = self.linkGroupMap.groupId
        self.linkId = self.linkGroupMap.linkId
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertGroup(self.group.id, self.group.name, self.group.public)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.title, 
                        self.link.description, self.link.typeName, self.link.modifiedAt)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertGroupTagMap(self.groupId, self.linkId)
        
        rows = db.selectFrom(self.conn, "link_group_map", "*", group_id=self.groupId, link_id=self.linkId)
        
        self.assertEqual(self.group.id, rows[0][0])
        self.assertEqual(self.link.id, rows[0][1])

    
    """ DATA TYPE TESTS """
    
    def testInsertInvalidGroupId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertGroupTagMap,
                          self.groupId + "e",
                          self.linkId)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertgroup ,
                         self.id[:-13], self.name, self.email)
        """
            
    def testInsertInvalidLinkId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertGroupTagMap,
                          self.groupId,
                          self.linkId + "e")
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertgroup ,
                         self.id[:-13], self.name, self.email)
        """

    """ NULL CONSTRAINS TESTS """    
        
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

    
    """ UNIQUE CONSTRAINS TESTS """
    def testInsertDublicategroupId(self):
        self.insertGroupTagMap(self.groupId, self.linkId)
        groupId = self.groupId
        self.__initDependencies()
        self.insertGroupTagMap(groupId,
                       self.linkId)
        
    def testInsertDublicateLinkId(self):
        self.insertGroupTagMap(self.groupId, self.linkId)
        linkId = self.linkId
        self.__initDependencies()
        self.insertGroupTagMap(self.groupId,
                       linkId)
        
    def testInsertDublicategroupAndLinkId(self):
        self.insertGroupTagMap(self.groupId, self.linkId)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertGroupTagMap,
                          self.groupId,
                          self.linkId)
    
    
    """ FOREIGN KEY CONSTRAINS TESTS """
    
    def testInsertNonExistinggroupId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertGroupTagMap,
                                mock.uuid(),
                                self.linkId)
        
    def testInsertNonExistingLinkId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertGroupTagMap,
                                self.groupId,
                                mock.uuid())
    
    #TODO: implement update entries tests
    #TODO: implement drop entries test