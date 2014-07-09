
import test.Tables as tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
    
    
class Link(tables.Tables):
    '''
    - Test: insertion and fetching data from/to table
    - Test: update entry and its references
    - Test: drop entry and its references
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
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
    