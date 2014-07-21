
import Tables as tables
import MockModule as mock
import db.main.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
        

class SearchTable(tables.Tables):
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
        self.userId = self.searchTable.userId
        self.linkId = self.searchTable.linkId
        self.groups = self.searchTable.groups
        self.tags = self.searchTable.tags
        self.text = self.searchTable.text
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.urlHash, self.link.title, self.link.description, self.link.typeName, self.link.modifiedAt)

    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        rows = db.selectFrom(self.conn, {"search_table"}, "*", id=self.user_id)
        
        self.assertEqual(self.user.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))
        self.assertEqual(self.groups, str(rows[0][2]))
        self.assertEqual(self.tags, str(rows[0][3]))
        self.assertEqual(self.text, str(rows[0][4]))

        
    ''' UPDATE TESTS '''

    def	testUpdateToExistingUserId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        searchTable = self.searchTable
        self.__initDependencies()
        db.updateInTable(self.conn, {"user_id":self.userId}, "search_table", user_id=searchTable.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=searchTable.userId)

        self.assertEqual(self.user.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))
        self.assertEqual(searchTable.groups, str(rows[0][2]))
        self.assertEqual(searchTable.tags, str(rows[0][3]))
        self.assertEqual(searchTable.text, str(rows[0][4]))

    def	testUpdateToNonExistingUserId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        _userId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                                   self.conn,
                                                   {"user_id":_userId},
                                                   "search_table",
                                                   user_id=self.userId)
    def	testUpdateToExistingLinkId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        searchTable = self.searchTable
        self.__initDependencies()
        db.updateInTable(self.conn, {"link_id":self.linkId}, "search_table", user_id=searchTable.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=searchTable.userId)

        self.assertEqual(self.user.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))
        self.assertEqual(searchTable.groups, str(rows[0][2]))
        self.assertEqual(searchTable.tags, str(rows[0][3]))
        self.assertEqual(searchTable.text, str(rows[0][4]))

    def	testUpdateToNonExistingLinkId(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        _linkId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                                   self.conn,
                                                   {"link_id":_linkId},
                                                   "search_table",
                                                   user_id=self.userId)
    def	testUpdateGroups(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        _groups = mock.randomText(256)
        db.updateInTable(self.conn, {"groups":_groups}, "search_table", user_id=self.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.user.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))
        self.assertEqual(_groups, str(rows[0][2]))
        self.assertEqual(self.tags, str(rows[0][3]))
        self.assertEqual(self.text, str(rows[0][4]))

    def	testUpdateTags(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        _tags = mock.randomText(256)
        db.updateInTable(self.conn, {"tags":_tags}, "search_table", user_id=self.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.user.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))
        self.assertEqual(self.groups, str(rows[0][2]))
        self.assertEqual(_tags, str(rows[0][3]))
        self.assertEqual(self.text, str(rows[0][4]))

    def	testUpdateText(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)

        _text = mock.randomText(2048)
        db.updateInTable(self.conn, {"text":_text}, "search_table", user_id=self.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)

        self.assertEqual(self.user.id, str(rows[0][0]))
        self.assertEqual(self.link.id, str(rows[0][1]))
        self.assertEqual(self.groups, str(rows[0][2]))
        self.assertEqual(self.tags, str(rows[0][3]))
        self.assertEqual(_text, str(rows[0][4]))


    ''' DROP TESTS '''

    def	testDropSearchTable(self):
        self.insertSearchTable(self.userId, self.linkId, self.groups, self.tags, self.text)
        db.deleteFromTable(self.conn, "search_table", user_id=self.userId)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.userId)
        self.assertEqual(rows, [])

