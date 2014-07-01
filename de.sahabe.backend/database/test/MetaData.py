'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
'''
import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class MetaData(Tables.Tables):
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
        self.linkId = self.metaData.linkId
        self.key = self.metaData.key
        self.value = self.metaData.value
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertLink(self.link.id, self.link.userId, self.link.url, self.link.title,
                        self.link.description, self.link.typeName, self.link.modifiedAt)
    
    def setUp(self):
        self.connect()
        self.__initDependencies()

    def tearDown(self):
        self.conn.close()


    ''' INSERTION TESTS '''

    def testInsertion(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        rows = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.linkId)

        self.assertEqual(self.linkId, rows[0][0])
        self.assertEqual(self.key, rows[0][1])
        self.assertEqual(self.value, rows[0][2])


    ''' UPDATE TESTS '''
    
    def testUpdateToExistingLinkId(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        metaData = self.metaData
        self.__initDependencies()
        db.updateInTable(self.conn, {"link_id":self.linkId}, "meta_data", link_id=metaData.linkId)
        
        rows = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.linkId)
        
        self.assertEqual(self.linkId, rows[0][0])
        self.assertEqual(metaData.key, rows[0][1])
        self.assertEqual(metaData.value, rows[0][2])
 
    def testUpdateToNonExistingLinkId(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        linkId= mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"link_id":linkId},
                                "meta_data",
                                link_id=self.linkId)

    def testUpdateKey(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        key = mock.randomName()
        db.updateInTable(self.conn, {"l_key":key}, "meta_data", link_id=self.linkId)
        
        rows = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.linkId)
        
        self.assertEqual(self.linkId, rows[0][0])
        self.assertEqual(key, rows[0][1])
        self.assertEqual(self.value, rows[0][2])
    
    def testUpdateValue(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        value = mock.randomName()
        db.updateInTable(self.conn, {"value":value}, "meta_data", link_id=self.linkId)
        
        rows = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.linkId)
        
        self.assertEqual(self.linkId, rows[0][0])
        self.assertEqual(self.key, rows[0][1])
        self.assertEqual(value, rows[0][2])
        
    
    ''' DROP TESTS '''
        
    def testMetaData(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        db.deleteFromTable(self.conn, "meta_data", link_id=self.linkId)
        rows = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.linkId)
        self.assertEquals(rows, [])
            
        
    ''' DATA TYPE TESTS '''
        
    def testInsertInvalidLinkId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertMetaData,
                         self.linkId + "e",
                         self.key,
                         self.value)
        
    def testInsertInvalidKey(self):
        key = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertMetaData,
                         self.linkId,
                         key,
                         self.value)
        
    def testInsertInvalidValue(self):
        value = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertMetaData,
                         self.linkId,
                         self.key,
                         value)
        
        
    ''' NULL CONSTRAINS TESTS '''
        
    def testInsertNoLinkId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'link_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "meta_data",
                          l_key=self.key,
                          value=self.value)
        
    def testInsertNoKey(self):
        self.assertRaisesRegexp(OperationalError, "Field 'l_key' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "meta_data",
                          link_id=self.linkId,
                          value=self.value)
        
    def testInsertNoValue(self):
        self.assertRaisesRegexp(OperationalError, "Field 'value' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "meta_data",
                          link_id=self.linkId,
                          l_key=self.key)
        
    
    ''' UNIQUE CONSTRAINS TESTS '''
        
    def testInsertDoublicateLinkId(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        linkId = self.linkId
        self.__initDependencies()
        self.insertMetaData(linkId,
                            self.key,
                            self.value)
        
    def testInsertDoublicateKey(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        key = self.key
        self.__initDependencies()
        self.insertMetaData(self.linkId,
                            key,
                            self.value)
        
    def testInsertDoublicatevalue(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        value = self.value
        self.__initDependencies()
        self.insertMetaData(self.linkId,
                            self.key,
                            value)
    
    def testInsertDoublicateLinkAndKey(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        linkId = self.linkId
        key = self.key
        self.__initDependencies()
        self.insertMetaData(linkId,
                            key,
                            self.value)
    
    def testInsertDoublicateLinkAndValue(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        linkId = self.linkId
        value = self.value
        self.__initDependencies()
        self.insertMetaData(linkId,
                            self.key,
                            value)
        
    def testInsertDoublicateKeyAndValue(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        key = self.key
        value = self.value
        self.__initDependencies()
        self.insertMetaData(self.linkId,
                            key,
                            value)
        
    def testInsertDoublicateLinkAndKeyAndValue(self):
        self.insertMetaData(self.linkId, self.key, self.value)
        linkId = self.linkId
        key = self.key
        value = self.value
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertMetaData,
                                linkId,
                                key,
                                value)
        
        
    ''' FOREIGN KEY CONSTRAINS TESTS '''
        
    def testInsertNonExistingLinkId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertMetaData,
                                mock.uuid(),
                                self.key,
                                self.value)
