'''
Created on Jun 27, 2014

@author: Maan Al Balkhi
'''

import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class LinkTagMap(Tables.Tables):
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
        self.tagId = self.linkTagMap.tagId
        self.linkId = self.linkTagMap.linkId
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertTag(self.tag.id, self.tag.name)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.title, 
                        self.link.description, self.link.typeName, self.link.modifiedAt)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertLinkTagMap(self.tagId, self.linkId)
        
        rows = db.selectFrom(self.conn, "link_tag_map", "*", tag_id=self.tagId, link_id=self.linkId)
        
        self.assertEqual(self.tag.id, rows[0][0])
        self.assertEqual(self.link.id, rows[0][1])

    
    """ DATA TYPE TESTS """
    
    def testInsertInvalidTagId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLinkTagMap,
                          self.tagId + "e",
                          self.linkId)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertTag ,
                         self.id[:-13], self.name, self.email)
        """
            
    def testInsertInvalidLinkId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLinkTagMap,
                          self.tagId,
                          self.linkId + "e")
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertTag ,
                         self.id[:-13], self.name, self.email)
        """

    """ NULL CONSTRAINS TESTS """    
        
    def testInsertNoTagId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'tag_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_tag_map",
                          link_id=self.linkId)
    
     
    
    def testInsertNoLinkId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'link_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link_tag_map",
                          tag_id=self.tagId)

    
    """ UNIQUE CONSTRAINS TESTS """
    def testInsertDublicateTagId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)
        tagId = self.tagId
        self.__initDependencies()
        self.insertLinkTagMap(tagId,
                       self.linkId)
        
    def testInsertDublicateLinkId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)
        linkId = self.linkId
        self.__initDependencies()
        self.insertLinkTagMap(self.tagId,
                       linkId)
        
    def testInsertDublicateTagAndLinkId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertLinkTagMap,
                          self.tagId,
                          self.linkId)
    
    
    """ FOREIGN KEY CONSTRAINS TESTS """
    
    def testInsertNonExistingTagId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertLinkTagMap,
                                mock.uuid(),
                                self.linkId)
        
    def testInsertNonExistingLinkId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertLinkTagMap,
                                self.tagId,
                                mock.uuid())
    
    #TODO: implement update tag.id tests
    #TODO: implement drop tag.id test    
    #TODO: implement update link.id tests
    #TODO: implement drop link.id test
    
    #TODO: implement update entries tests
    #TODO: implement drop entries test