
import test.Tables as tables
import test.MockModule as mock
import impl.DBApiModule as db
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
        self.tagId = self.link_tag_map.tagId
        self.linkId = self.link_tag_map.linkId
        self.insertTag(self.tag.id, self.tag.name)
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.user_id, self.link.url, self.link.url_hash, self.link.title, self.link.description, self.link.type_name, self.link.modified_at)

    def setUp(self):
        self.connect()
        self.__initDependencies()
    
    def tearDown(self):
        self.conn.close()
    