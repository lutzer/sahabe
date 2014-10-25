
import Tables as tables
import MockModule as mock
import app.db.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
        

class Tag(tables.Tables):
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
        self.id = self.tag.id
        self.name = self.tag.name

    def setUp(self):
        self.connect()
        self.__initDependencies()
        
    def tearDown(self):
        self.conn.close()
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertTag(self.id, self.name)

        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)
        
        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(self.name, str(rows[0][1]))

        
    ''' UPDATE TESTS '''

    def	testUpdateId(self):
        self.insertTag(self.id, self.name)

        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "tag", id=self.id)
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=_id)

        self.assertEqual(_id, str(rows[0][0]))
        self.assertEqual(self.name, str(rows[0][1]))

    def	testUpdateName(self):
        self.insertTag(self.id, self.name)

        _name = mock.randomText(64)
        db.updateInTable(self.conn, {"name":_name}, "tag", id=self.id)
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)

        self.assertEqual(self.id, str(rows[0][0]))
        self.assertEqual(_name, str(rows[0][1]))


    ''' DROP TESTS '''

    def	testDropTag(self):
        self.insertTag(self.id, self.name)
        db.deleteFromTable(self.conn, "tag", id=self.id)
        rows = db.selectFrom(self.conn, {"tag"}, "*", id=self.id)
        self.assertEqual(rows, [])

    def	testDropLinkTagMapByTag(self):
        self.insertTag(self.id, self.name)
        self.insertLinkTagMap(self.linkTagMap.tagId, self.linkTagMap.linkId)
        db.deleteFromTable(self.conn, "tag", id=self.id)
        rows = db.selectFrom(self.conn, {"link_tag_map"}, "*", tag_id=self.linkTagMap.tagId)
        self.assertEqual(rows, [])

