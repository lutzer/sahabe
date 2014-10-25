'''
Created on Jun 14, 2014

@author: Maan Al Balkhi
'''
import Tables
import app.db.MockModule as mock
import app.db.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class User(Tables.Tables):
    '''
    - Test: insertion and fetching data from/to table
    - Test: update entry and its references
    - Test: drop entry and its references
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    ''' 
    
    def setUp(self):
        self.connect()
        self.initDBMockContents()
        self.id = self.user.id
        self.name = self.user.name
        self.email = self.user.email
        
    def tearDown(self):
        self.conn.close()
        
        
    ''' INSERTION TESTS '''
    
    def testInsertion(self):
        self.insertUser(self.id, self.name, self.email)
        
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(self.email, rows[0][2])


    ''' UPDATE TESTS '''

    def testId(self):
        self.insertUser(self.id, self.name, self.email)
        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "user", id=self.id)
        
        rows = db.selectFrom(self.conn, {"user"}, "*", id=_id)
        
        self.assertEqual(_id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(self.email, rows[0][2])
        
    def testName(self):
        self.insertUser(self.id, self.name, self.email)
        name = mock.randomText()
        db.updateInTable(self.conn, {"name":name}, "user", id=self.id)
        
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(name, rows[0][1])
        self.assertEqual(self.email, rows[0][2])
        
    def testEmail(self):
        self.insertUser(self.id, self.name, self.email)
        email = mock.randomText()
        db.updateInTable(self.conn, {"email":email}, "user", id=self.id)
        
        rows = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.name, rows[0][1])
        self.assertEqual(email, rows[0][2])
        
    def testIdReferencedToLink(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "user",
                                id=self.id)
        
    def testIdReferencedToSearchTable(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertSearchTable(self.searchTable.userId,
                               self.searchTable.linkId,
                               self.searchTable.groups,
                               self.searchTable.tags,
                               self.searchTable.text)
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "user",
                                id=self.id)
        
    def testIdReferencedToPW(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertPW(self.pw.userId, self.pw.value, self.pw.salt)
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "user",
                                id=self.id)

  
    ''' DROP TESTS '''
        
    def testDropUser(self):
        self.insertUser(self.id, self.name, self.email)
        
        db.deleteFromTable(self.conn, "user", id=self.id) 
        row = db.selectFrom(self.conn, {"user"}, "*", id=self.id)
        self.assertEqual(row, [])
    
    def testDropPWByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertPW(self.pw.userId, self.pw.value, self.pw.salt)
        
        db.deleteFromTable(self.conn, "user", id=self.id) 
        row = db.selectFrom(self.conn, {"pw_hash"}, "*", user_id=self.id)
        self.assertEqual(row, [])
        
    def testDropLinkByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        
        db.deleteFromTable(self.conn, "user", id=self.id) 
        row = db.selectFrom(self.conn, {"link"}, "*", id=self.link.id)
        self.assertEqual(row, [])
        
    def testDropSearchTableByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertSearchTable(self.searchTable.userId,
                               self.searchTable.linkId,
                               self.searchTable.groups,
                               self.searchTable.tags,
                               self.searchTable.text)
        
        db.deleteFromTable(self.conn, "user", id=self.id)
        row = db.selectFrom(self.conn, {"search_table"}, "*" , link_id=self.searchTable.linkId)
        self.assertEqual(row, [])
        
    def testDropTagByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertTag(self.tag.id, self.tag.name)
        
        db.deleteFromTable(self.conn, "user", id=self.id)
        row = db.selectFrom(self.conn, {"tag"}, "*" , id=self.tag.id)
        # FIXME: when a user is deleted all of his tags must be removed 
        self.assertEqual(row, [])
        
    def testDropGroupByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertGroup(self.group.id, self.group.name, self.group.public)
        
        db.deleteFromTable(self.conn, "user", id=self.id)
        row = db.selectFrom(self.conn, {"link_group"}, "*" , id=self.group.id)
        # FIXME: when a user is deleted all of his groups must be removed
        self.assertEqual(row, [])
        
    def testDropLinkTagMapByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertTag(self.tag.id, self.tag.name)
        self.insertLinkTagMap(self.linkTagMap.tagId, self.linkTagMap.linkId)
        
        db.deleteFromTable(self.conn, "user", id=self.id)
        row = db.selectFrom(self.conn, {"link_tag_map"}, "*", link_id=self.linkTagMap.linkId)
        self.assertEqual(row, [])
        
    def testDropLinkGroupMapByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertGroup(self.group.id, self.group.name, self.group.public)
        self.insertLinkGroupMap(self.linkGroupMap.groupId, self.linkGroupMap.linkId)
        
        db.deleteFromTable(self.conn, "user", id=self.id)
        row = db.selectFrom(self.conn, {"link_group_map"}, "*", link_id=self.linkGroupMap.linkId)
        self.assertEqual(row, [])
       
    def testDropMetaDataByUser(self):
        self.insertUser(self.id, self.name, self.email)
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash,
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertMetaData(self.metaData.linkId, self.metaData.key, self.metaData.value)
        
        db.deleteFromTable(self.conn, "user", id=self.id)
        row = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.metaData.linkId)
        self.assertEqual(row, [])
    
    
    ''' DATA TYPE TESTS '''
    
    def testInsertInvalidId(self):
        self.assertRaisesRegexp(DataError, "Data too long", self.insertUser,
                          self.id + "e",
                          self.name,
                          self.email)
        ''' insert too short '''
        # FIXME: what's about UUID length constrains? 
        '''
        self.assertRaises(DataError, self.insertUser ,
                         self.id[:-13], self.name, self.email)
        '''
        
    def testInsertInvalidName(self):
        name = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertUser,
                          self.id,
                          name,
                          self.email)
    
    def testInsertInvalidEmail(self):
        email = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertUser,
                          self.id,
                          self.name,
                          email)


    
    ''' NULL CONSTRAINS TESTS '''    
        
    def testInsertNoId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "user",
                          name=self.name,
                          email=self.email)
        
    def testInsertNoName(self):
        self.assertRaisesRegexp(OperationalError, "Field 'name' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "user",
                          id=self.id,
                          email=self.email)
        
    def testInsertNoEmail(self):
        self.assertRaisesRegexp(OperationalError, "Field 'email' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "user",
                          id=self.id,
                          name=self.name)
        
    
    ''' UNIQUE CONSTRAINS TESTS '''
        
    def testInsertDublicateId(self):
        self.insertUser(self.id, self.name, self.email)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertUser,
                          self.id,
                          mock.randomText(),
                          mock.randomEmail())
        
    def testInsertDublicateName(self):
        self.insertUser(self.id, self.name, self.email)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertUser,
                          mock.uuid(),
                          self.name,
                          mock.randomEmail())
        
    def testInsertDublicateEmail(self):
        self.insertUser(self.id, self.name, self.email)
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertUser,
                          mock.uuid(),
                          mock.randomText(),
                          self.email)
