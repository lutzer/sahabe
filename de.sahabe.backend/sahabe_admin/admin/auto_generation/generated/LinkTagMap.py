
import Tables as tables
import MockModule as mock
import admin.main.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
        

class LinkTagMap(tables.Tables):
    '''
    - Test: insertion and fetching data from/to table
    - Test: update entry and its references
    - Test: drop entry and its references
    - Test: references.
    - Test: inserting invalid modifiedAt
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    - Test: FOREIGN KEY CONSTRAINS
    '''     
        
        
    def __initDependencies(self):
        self.initDBMockContents()
        self.tagId = self.linkTagMap.tagId
        self.linkId = self.linkTagMap.linkId
        self.insertTag(self.tag.id, self.tag.name)
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.urlHash, self.link.title, self.link.description, self.link.typeName, self.link.modifiedAt)

    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertLinkTagMap(self.tagId, self.linkId)

        rows = db.selectFrom(self.conn, {"link_tag_map"}, "*", id=self.tag_id)
        
        self.assertEqual(self.tag.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))

        
    ''' UPDATE TESTS '''

    def	testUpdateToExistingTagId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)

        linkTagMap = self.linkTagMap
        self.__initDependencies()
        db.updateInTable(self.conn, {"tag_id":self.tagId}, "link_tag_map", tag_id=linkTagMap.tagId)
        rows = db.selectFrom(self.conn, {"link_tag_map"}, "*", tag_id=linkTagMap.tagId)

        self.assertEqual(self.tag.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))

    def	testUpdateToNonExistingTagId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)

        _tagId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                                   self.conn,
                                                   {"tag_id":_tagId},
                                                   "link_tag_map",
                                                   tag_id=self.tagId)
    def	testUpdateToExistingLinkId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)

        linkTagMap = self.linkTagMap
        self.__initDependencies()
        db.updateInTable(self.conn, {"link_id":self.linkId}, "link_tag_map", tag_id=linkTagMap.tagId)
        rows = db.selectFrom(self.conn, {"link_tag_map"}, "*", tag_id=linkTagMap.tagId)

        self.assertEqual(self.tag.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))

    def	testUpdateToNonExistingLinkId(self):
        self.insertLinkTagMap(self.tagId, self.linkId)

        _linkId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                                   self.conn,
                                                   {"link_id":_linkId},
                                                   "link_tag_map",
                                                   tag_id=self.tagId)

    ''' DROP TESTS '''

    def	testDropLinkTagMap(self):
        self.insertLinkTagMap(self.tagId, self.linkId)
        db.deleteFromTable(self.conn, "link_tag_map", tag_id=self.tagId)
        rows = db.selectFrom(self.conn, {"link_tag_map"}, "*", tag_id=self.tagId)
        self.assertEqual(rows, [])

