
import test.Tables as tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
    
    
class User(tables.Tables):
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
        self.id = self.user.id
        self.name = self.user.name
        self.email = self.user.email

    def setUp(self):
        self.connect()
        self.__initDependencies()
    
    def tearDown(self):
        self.conn.close()
    