'''
Created on Jun 15, 2014

@author: maan al balkhi
'''
import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class SearchTable(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    """
    
    def __initDependencies(self):
        self.initDBMockContents()
        self.userId = self.searchTable.userId
        self.linkId = self.searchTable.linkId
        self.groups = self.searchTable.groups
        self.tags = self.searchTable.tags
        self.text =self.searchTable.text
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.title, 
                        self.link.description, self.link.typeName, self.link.modifiedAt)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()

    def tearDown(self):
        self.conn.close()


    def testInsertion(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        rows = db.selectFrom(self.conn, "search_table", "*", user_id=self.userId)

        self.assertEqual(self.user.id, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])
        self.assertEqual(self.groups, rows[0][2])
        self.assertEqual(self.tags, rows[0][3])
        self.assertEqual(self.text, rows[0][4])
        
        
    """ DATA TYPE TESTS """
        
    def testInsertInvalidUserId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId + "e",
                         self.linkId,
                         self.groups,
                         self.tags,
                         self.text)
        
    def testInsertInvalidLinkId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId + "e",
                         self.groups,
                         self.tags,
                         self.text)
    def testInsertInvalidGroups(self):
        groups = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId,
                         groups,
                         self.tags,
                         self.text)
        
    def testInsertInvalidTags(self):
        tags = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId,
                         self.groups,
                         tags,
                         self.text)
    
    def testInsertInvalidText(self):
        text = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId,
                         self.groups,
                         self.tags,
                         text)
        
        
    """ NULL CONSTRAINS TESTS """
        
    def testInsertNoUserId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'user_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "search_table",
                          link_id=self.linkId,
                          groups=self.groups,
                          tags=self.tags,
                          text=self.text)
        
    def testInsertNoLinkId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'link_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "search_table",
                          user_id=self.userId,
                          groups=self.groups,
                          tags=self.tags,
                          text=self.text)
        
    def testInsertNoGroups(self):
        db.insertToTable(self.conn, "search_table",
                         user_id=self.userId,
                         link_id=self.linkId,
                         tags=self.tags,
                         text=self.text)
        
    def testInsertNoTags(self):
        db.insertToTable(self.conn, "search_table",
                         user_id=self.userId,
                         link_id=self.linkId,
                         groups=self.groups,
                         text=self.text)
        
    def testInsertNoText(self):
        db.insertToTable(self.conn, "search_table",
                         user_id=self.userId,
                         link_id=self.linkId,
                         groups=self.groups,
                         tags=self.tags)
    
    
    """ UNIQUE CONSTRAINS TESTS """
    # FIXME: what's about UNIQUE constrains? 
        
    def testInsertDoublicateId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        userId=self.userId
        self.__initDependencies()
        self.insertSearchTable(userId,
                               self.linkId,
                               self.groups,
                               self.tags,
                               self.text)
        
    def testInsertDoublicateLinkId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        linkId=self.linkId
        self.__initDependencies()
        self.insertSearchTable(self.userId,
                               linkId,
                               self.groups,
                               self.tags,
                               self.text)
        
    def testInsertDoublicatUserAndLinkId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        userId=self.userId
        linkId=self.linkId
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertSearchTable,
                                userId,
                                linkId,
                                self.groups,
                                self.tags,
                                self.text)
        
    def testInsertDoublicateGroups(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        groups=self.groups
        self.__initDependencies()
        self.insertSearchTable(self.userId,
                               self.linkId,
                               groups,
                               self.tags,
                               self.text)
        
    def testInsertDoublicatetags(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        tags=self.tags
        self.__initDependencies()
        self.insertSearchTable(self.userId,
                            self.linkId,
                            self.groups,
                            tags,
                            self.text)
    
    def testInsertDoublicateText(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        text=self.text
        self.__initDependencies()
        self.insertSearchTable(self.userId,
                            self.linkId,
                            self.groups,
                            self.tags,
                            text)
