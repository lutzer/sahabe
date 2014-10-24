'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
'''
import Tables
import db.main.MockModule as mock
import db.main.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class SearchTable(Tables.Tables):
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
        self.userId = self.searchTable.userId
        self.linkId = self.searchTable.linkId
        self.groups = self.searchTable.groups
        self.tags = self.searchTable.tags
        self.text =self.searchTable.text
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.urlHash,
                        self.link.title, self.link.description, self.link.typeName, self.link.modifiedAt)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()

    def tearDown(self):
        self.conn.close()


    ''' INSERTTON TESTS '''

    def testInsertion(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId, link_id=self.linkId)

        self.assertEqual(self.user.id, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])
        self.assertEqual(self.groups, rows[0][2])
        self.assertEqual(self.tags, rows[0][3])
        self.assertEqual(self.text, rows[0][4])
    
    
    ''' UPDATE TESTS '''
    
    def testUpdateToExistingUserId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        searchTable=self.searchTable
        self.__initDependencies()
        db.updateInTable(self.conn, {"user_id":self.userId}, "search_table", user_id=searchTable.userId)
        
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.user.id, rows[0][0])
        self.assertEqual(searchTable.linkId, rows[0][1])
        self.assertEqual(searchTable.groups, rows[0][2])
        self.assertEqual(searchTable.tags, rows[0][3])
        self.assertEqual(searchTable.text, rows[0][4])
      
    def testUpdateToNonExistingUserId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        userId=mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                self.conn,
                                {"user_id":userId},
                                "search_table",
                                user_id=self.userId)
        
        
    def testUpdateToExistingLinkId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        searchTable=self.searchTable
        self.__initDependencies()
        db.updateInTable(self.conn, {"link_id":self.linkId}, "search_table", user_id=searchTable.userId)
        
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=searchTable.userId)

        self.assertEqual(searchTable.userId, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])
        self.assertEqual(searchTable.groups, rows[0][2])
        self.assertEqual(searchTable.tags, rows[0][3])
        self.assertEqual(searchTable.text, rows[0][4])
          
    def testUpdateToNonExistingLinkId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        linkId=mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"link_id":linkId},
                                "search_table",
                                user_id=self.userId)
        
    def testUpdateGroups(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        groups=mock.randomText()
        db.updateInTable(self.conn, {"groups":groups}, "search_table", user_id=self.userId)
        
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.userId, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])
        self.assertEqual(groups, rows[0][2])
        self.assertEqual(self.tags, rows[0][3])
        self.assertEqual(self.text, rows[0][4])
        
    def testUpdateTags(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        tags=mock.randomText()
        db.updateInTable(self.conn, {"tags":tags}, "search_table", user_id=self.userId)
        
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.userId, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])
        self.assertEqual(self.groups, rows[0][2])
        self.assertEqual(tags, rows[0][3])
        self.assertEqual(self.text, rows[0][4])
        
    def testUpdateText(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        text=mock.randomText()
        db.updateInTable(self.conn, {"text":text}, "search_table", user_id=self.userId)
        
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.userId, rows[0][0])
        self.assertEqual(self.linkId, rows[0][1])
        self.assertEqual(self.groups, rows[0][2])
        self.assertEqual(self.tags, rows[0][3])
        self.assertEqual(text, rows[0][4])

    
    ''' DROP TESTS '''
        
    def testDropSearchTable(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        db.deleteFromTable(self.conn, "search_table", user_id=self.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)
        self.assertEquals(rows, [])
        
        
    ''' DATA TYPE TESTS '''
        
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
        groups = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId,
                         groups,
                         self.tags,
                         self.text)
        
    def testInsertInvalidTags(self):
        tags = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId,
                         self.groups,
                         tags,
                         self.text)
    
    def testInsertInvalidText(self):
        text = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertSearchTable,
                         self.userId,
                         self.linkId,
                         self.groups,
                         self.tags,
                         text)
        
        
    ''' NULL CONSTRAINS TESTS '''
        
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
    
    
    ''' UNIQUE CONSTRAINS TESTS '''
        
    def testInsertDoublicateUserId(self):
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
        # FIXME: a link belongs only to one user. insertion should throw ERROR
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertSearchTable,
                                self.userId,
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
        
        
    ''' FOREIGN KEY CONSTRAINS TESTS '''
    
    def testInsertNonExistingUserId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertSearchTable,
                                mock.uuid(),
                                self.linkId,
                                self.groups,
                                self.tags,
                                self.text)
        
    def testInsertNonExistingLinkId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertSearchTable,
                                self.userId,
                                mock.uuid(),
                                self.groups,
                                self.tags,
                                self.text)
