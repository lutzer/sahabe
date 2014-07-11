
import Tables as tables
import MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
        

class Link(tables.Tables):
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
        self.id = self.link.id
        self.userId = self.link.userId
        self.url = self.link.url
        self.urlHash = self.link.urlHash
        self.title = self.link.title
        self.description = self.link.description
        self.typeName = self.link.typeName
        self.modifiedAt = self.link.modifiedAt
        self.insertUser(self.user.id, self.user.name, self.user.email)

    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

        
    ''' UPDATE TESTS '''

    def	testUpdateId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=_id)

        self.assertEqual(_id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def	testUpdateToExistingUserId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        link = self.link
        self.__initDependencies()
        db.updateInTable(self.conn, {"user_id":self.userId}, "link", id=link.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=link.id)

        self.assertEqual(link.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(link.url, str(rows[0][2]))
        self.assertEqual(link.urlHash, str(rows[0][3]))
        self.assertEqual(link.title, str(rows[0][4]))
        self.assertEqual(link.description, str(rows[0][5]))
        self.assertEqual(link.typeName, str(rows[0][6]))
        self.assertEqual(link.modifiedAt, str(rows[0][7]))

    def	testUpdateToNonExistingUserId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _userId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                                   self.conn,
                                                   {"user_id":_userId},
                                                   "link",
                                                   id=self.id)
    def	testUpdateUrl(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _url = mock.randomText(2048)
        db.updateInTable(self.conn, {"url":_url}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(_url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def	testUpdateUrlHash(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _urlHash = mock.MD5()
        db.updateInTable(self.conn, {"url_hash":_urlHash}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(_urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def	testUpdateTitle(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _title = mock.randomText(256)
        db.updateInTable(self.conn, {"title":_title}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(_title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def	testUpdateDescription(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _description = mock.randomText(256)
        db.updateInTable(self.conn, {"description":_description}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(_description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def	testUpdateTypeName(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _typeName = mock.randomText(64)
        db.updateInTable(self.conn, {"type_name":_typeName}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(_typeName, str(rows[0][6]))
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def	testUpdateModifiedAt(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)

        _modifiedAt = mock.timeStamp()
        db.updateInTable(self.conn, {"modified_at":_modifiedAt}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.user.id, str(rows[0][1]))
        self.assertEqual(self.url, str(rows[0][2]))
        self.assertEqual(self.urlHash, str(rows[0][3]))
        self.assertEqual(self.title, str(rows[0][4]))
        self.assertEqual(self.description, str(rows[0][5]))
        self.assertEqual(self.typeName, str(rows[0][6]))
        self.assertEqual(_modifiedAt, str(rows[0][7]))


    ''' DROP TESTS '''

    def	testDropLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)
        db.deleteFromTable(self.conn, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        self.assertEqual(rows, [])

    def	testDropSearchTableByLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)
        self.insertSearchTable(self.searchTable.userId, self.searchTable.linkId, self.searchTable.groups, self.searchTable.tags, self.searchTable.text)
        db.deleteFromTable(self.conn, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.searchTable.userId)
        self.assertEqual(rows, [])

    def	testDropLinkTagMapByLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title, self.description, self.typeName, self.modifiedAt)
        self.insertLinkTagMap(self.linkTagMap.tagId, self.linkTagMap.linkId)
        db.deleteFromTable(self.conn, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link_tag_map"}, "*", tag_id=self.linkTagMap.tagId)
        self.assertEqual(rows, [])

