
import Tables as tables
import MockModule as mock
import db.main.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
        

class User(tables.Tables):
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
        self.id = self.user.id
        self.name = self.user.name
        self.email = self.user.email

    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertUser(self.id, self.name, self.email)

        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        
        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.name, str(rows[0][1]))
        self.assertEqual(self.email, str(rows[0][2]))

        
    ''' UPDATE TESTS '''

    def	testUpdateId(self):
        self.insertUser(self.id, self.name, self.email)

        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "user", id=self.id)
        rows = db.selectFrom(self.conn, {"user"}, "*", id=_id)

        self.assertEqual(_id, str(rows[0][0]))
        self.assertEqual(self.name, str(rows[0][1]))
        self.assertEqual(self.email, str(rows[0][2]))

    def	testUpdateName(self):
        self.insertUser(self.id, self.name, self.email)

        _name = mock.randomText(64)
        db.updateInTable(self.conn, {"name":_name}, "user", id=self.id)
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(_name, str(rows[0][1]))
        self.assertEqual(self.email, str(rows[0][2]))

    def	testUpdateEmail(self):
        self.insertUser(self.id, self.name, self.email)

        _email = mock.randomText(64)
        db.updateInTable(self.conn, {"email":_email}, "user", id=self.id)
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.name, str(rows[0][1]))
        self.assertEqual(_email, str(rows[0][2]))


    ''' DROP TESTS '''

    def	testDropUser(self):
        self.insertUser(self.id, self.name, self.email)
        db.deleteFromTable(self.conn, "user", id=self.id)
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        self.assertEqual(rows, [])

    def	testDropLinkByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.urlHash, self.link.title, self.link.description, self.link.typeName, self.link.modifiedAt)
        db.deleteFromTable(self.conn, "user", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.link.id)
        self.assertEqual(rows, [])

    def	testDropSearchTableByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertSearchTable(self.searchTable.userId, self.searchTable.linkId, self.searchTable.groups, self.searchTable.tags, self.searchTable.text)
        db.deleteFromTable(self.conn, "user", id=self.id)
        rows = db.selectFrom(self.conn, {"search_table"}, "*", user_id=self.searchTable.userId)
        self.assertEqual(rows, [])

