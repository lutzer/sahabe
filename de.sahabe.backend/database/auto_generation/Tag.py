
import test.Tables as tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
    
    
class Tag(tables.Tables):
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
        self.id = self.tag.id
        self.name = self.tag.name

    def setUp(self):
        self.connect()
        self.__initDependencies()
    
    def tearDown(self):
        self.conn.close()
    