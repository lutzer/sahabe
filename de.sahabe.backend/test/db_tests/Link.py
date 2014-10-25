'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
'''

import Tables
import app.db.MockModule as mock
import app.db.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class Link(Tables.Tables):
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
        self.desc = self.link.description
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
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName , self.modifiedAt)
        
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(self.title, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(self.typeName, rows[0][6])
        self.assertEqual(self.modifiedAt, str(rows[0][7]))
    
    
    ''' UPDATE TESTS '''
    
    def testUpdateId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        _id = mock.uuid()
        db.updateInTable(self.conn, {"id":_id}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=_id)
        
        self.assertEqual(_id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(self.title, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(self.typeName, rows[0][6])
        self.assertEqual(self.modifiedAt, str(rows[0][7]))

    def testUpdateToExistingUserId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        #save link data and reinit. 
        link = self.link
        self.__initDependencies()
        db.updateInTable(self.conn, {"user_id":self.userId}, "link", id=link.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=link.id)
        
        self.assertEqual(link.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(link.url, rows[0][2])
        self.assertEqual(link.urlHash, rows[0][3])
        self.assertEqual(link.title, rows[0][4])
        self.assertEqual(link.description, rows[0][5])
        self.assertEqual(link.typeName, rows[0][6])
        self.assertEqual(link.modifiedAt, str(rows[0][7]))
   
    def testUpdateToNonExistingUserId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        userId = mock.uuid()
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                self.conn,
                                {"user_id":userId},
                                "link",
                                id=self.id)
        
    def testUpdateUrl(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        url = mock.randomText()
        db.updateInTable(self.conn, {"url":url}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(self.title, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(self.typeName, rows[0][6])
        self.assertEqual(self.modifiedAt, str(rows[0][7]))
        
    def testUpdateTitle(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        title = mock.randomText()
        db.updateInTable(self.conn, {"title":title}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(title, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(self.typeName, rows[0][6])
        self.assertEqual(self.modifiedAt, str(rows[0][7]))
    
    def testUpdateDescription(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        desc = mock.randomText()
        db.updateInTable(self.conn, {"description":desc}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(self.title, rows[0][4])
        self.assertEqual(desc, rows[0][5])
        self.assertEqual(self.typeName, rows[0][6])
        self.assertEqual(self.modifiedAt, str(rows[0][7]))
        
    def testUpdateTypeName(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        typeName = mock.randomText()
        db.updateInTable(self.conn, {"type_name":typeName}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(self.title, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(typeName, rows[0][6])
        self.assertEqual(self.modifiedAt, str(rows[0][7]))
         
    def testUpdateModifietAt(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        modifiedAt = mock.timeStamp()
        db.updateInTable(self.conn, {"modified_at":modifiedAt}, "link", id=self.id)
        rows = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.urlHash, rows[0][3])
        self.assertEqual(self.title, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(self.typeName, rows[0][6])
        self.assertEqual(modifiedAt, str(rows[0][7]))
        
    def testUpdateIdReferencedToSearchTable(self):
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
                                "link",
                                id=self.id)
    
    def testUpdateIdReferencedToLinkTagMap(self):
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
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "link",
                                id=self.id)
        
    def testUpdateIdReferencedToLinkGroupMap(self):
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
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "link",
                                id=self.id)
        
    def testUpdateIdReferencedToMetaData(self):
        self.insertLink(self.link.id,
                        self.link.userId,
                        self.link.url,
                        self.link.urlHash, 
                        self.link.title,
                        self.link.description,
                        self.link.typeName,
                        self.link.modifiedAt)
        self.insertMetaData(self.metaData.linkId, self.metaData.key, self.metaData.value)
        
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", db.updateInTable,
                                self.conn,
                                {"id":mock.uuid()},
                                "link",
                                id=self.id)    
           
    
    ''' DROP TESTS '''
        
    def testDropLink(self):
        self.insertLink(self.id, self.userId, self.url, self.link.urlHash, self.title,
                        self.desc, self.typeName , self.modifiedAt)
        db.deleteFromTable(self.conn, "link", id=self.id) 
        row = db.selectFrom(self.conn, {"link"}, "*", id=self.id)
        self.assertEqual(row, [])
        
    def testDropSearchTableByLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName , self.modifiedAt)
        self.insertSearchTable(self.searchTable.userId,
                               self.searchTable.linkId,
                               self.searchTable.groups,
                               self.searchTable.tags,
                               self.searchTable.text)
        db.deleteFromTable(self.conn, "link", id=self.id)
        row = db.selectFrom(self.conn, {"search_table"}, "*" , link_id=self.searchTable.linkId)
        self.assertEqual(row, [])
        
    def testDropLinkTagMapByLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName , self.modifiedAt)
        self.insertTag(self.tag.id, self.tag.name)
        self.insertLinkTagMap(self.linkTagMap.tagId, self.linkTagMap.linkId)
        
        db.deleteFromTable(self.conn, "link", id=self.id)
        row = db.selectFrom(self.conn, {"link_tag_map"}, "*", link_id=self.linkTagMap.linkId)
        self.assertEqual(row, [])
        
    def testDropLinkGroupMapByLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName , self.modifiedAt)
        self.insertGroup(self.group.id, self.group.name, self.group.public)
        self.insertLinkGroupMap(self.linkGroupMap.groupId, self.linkGroupMap.linkId)
        
        db.deleteFromTable(self.conn, "link", id=self.id)
        row = db.selectFrom(self.conn, {"link_group_map"}, "*", link_id=self.linkGroupMap.linkId)
        self.assertEqual(row, [])
       
    def testDropMetaDataByLink(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName , self.modifiedAt)
        self.insertMetaData(self.metaData.linkId, self.metaData.key, self.metaData.value)
        
        db.deleteFromTable(self.conn, "link", id=self.id)
        row = db.selectFrom(self.conn, {"meta_data"}, "*", link_id=self.metaData.linkId)
        self.assertEqual(row, []) 
        
        
    ''' DATA TYPE TESTS '''

    def testInsertInvalidId(self):
        self.assertRaises(DataError, self.insertLink ,
                         self.id + "e", self.userId, self.url, self.urlHash, self.title,
                         self.desc, self.typeName, self.modifiedAt)
        ''' insert too short '''
        # FIXME: what's about UUID length constrains? 
        '''
        self.assertRaises(DataError, self.insertLink ,
                         self.id[:-13], self.title, self.email)
        '''
        
    def testInsertInvalidUserId(self):
        self.assertRaisesRegexp(DataError, "Data too long" , self.insertLink,
                         self.id,
                         mock.uuid() + "e",
                         self.url,
                         self.urlHash,
                         self.title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)

    def testInsertInvalidUrl(self):
        url = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         url,
                         self.urlHash, 
                         self.title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertInvalidTitle(self):
        title = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.urlHash, 
                         title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertInvaliddescription(self):
        desc = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.urlHash, 
                         self.title,
                         desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertInvalidTypeName(self):
        typeName = mock.randomFixedLengthText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.urlHash, 
                         self.title,
                         self.desc,
                         typeName,
                         self.modifiedAt)
        
    def testInsertInvalidModifiedAt(self):
        self.assertRaisesRegexp(OperationalError, "Incorrect datetime value", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.urlHash, 
                         self.title,
                         self.desc,
                         self.typeName,
                         mock.randomText(64))
       
    
    ''' NULL CONSTRAINS TESTS ''' 
        
    def testInsertNoId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link",
                          user_id=self.userId,
                          url=self.url,
                          title=self.title,
                          description=self.desc,
                          type_name=self.typeName,
                          modified_at=self.modifiedAt)
        
    def testInsertNoUserId(self):
        self.assertRaisesRegexp(OperationalError, "Field 'user_id' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link",
                          id=self.id,
                          url=self.url,
                          title=self.title,
                          description=self.desc,
                          type_name=self.typeName,
                          modified_at=self.modifiedAt)
                
    def testInsertNoUrl(self):
        self.assertRaisesRegexp(OperationalError, "Field 'url' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          title=self.title,
                          description=self.desc,
                          type_name=self.typeName,
                          modified_at=self.modifiedAt)

    def testInsertNoTitle(self):
        db.insertToTable(self.conn, "link",
                         id=self.id,
                         user_id=self.userId,
                         url=self.url,
                         url_hash=self.urlHash, 
                         description=self.desc,
                         type_name=self.typeName,
                         modified_at=self.modifiedAt)
    
    def testInsertNoDescription(self):
        db.insertToTable(self.conn, "link",
                         id=self.id,
                         user_id=self.userId,
                         url=self.url,
                         url_hash=self.urlHash,
                         title=self.title,
                         type_name=self.typeName,
                         modified_at=self.modifiedAt)
        
    
    def testInsertNoTypeName(self):
        db.insertToTable(self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          url=self.url,
                          url_hash=self.urlHash,
                          title=self.title,
                          description=self.desc,
                          modified_at=self.modifiedAt)
        
    def testInsertNoModifiedAt(self):
        self.assertRaisesRegexp(OperationalError, "Field 'modified_at' doesn't have a default value",
                          db.insertToTable,
                          self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          url=self.url,
                          url_hash=self.urlHash, 
                          title=self.title,
                          description=self.desc,
                          type_name=self.typeName)


    ''' UNIQUE CONSTRAINS TESTS '''    

    def testInsertDublicateId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        _id = self.id
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertLink,
                          _id,
                          self.userId,
                          self.url,
                          self.urlHash,
                          self.title,
                          self.desc,
                          self.typeName,
                          self.modifiedAt)
        
    def testInsertDublicateUserId(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        userId = self.userId
        self.__initDependencies()
        self.insertLink(self.id,
                         userId,
                         self.url,
                         self.urlHash,
                         self.title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertDublicateUrl(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        url = self.url
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        url,
                        self.urlHash,
                        self.title,
                        self.desc,
                        self.typeName,
                        self.modifiedAt)
    
    def testInsertDublicateTitle(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        title = self.title
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.url,
                        self.urlHash,
                        title,
                        self.desc,
                        self.typeName,
                        self.modifiedAt)
        
    def testInsertDublicateDescription(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        desc = self.desc
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.url,
                        self.urlHash,
                        self.title,
                        desc,
                        self.typeName,
                        self.modifiedAt)
        
    def testInsertDublicateModifiedAt(self):
        self.insertLink(self.id, self.userId, self.url, self.urlHash, self.title,
                        self.desc, self.typeName, self.modifiedAt)
        modifiedAt = self.modifiedAt
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.url,
                        self.urlHash,
                        self.title,
                        self.desc,
                        self.typeName,
                        modifiedAt)
        
        
    ''' FOREIGN KEY CONSTRAINS TESTS '''
    
    def testInsertNonExistingUserId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertLink,
                                self.id,
                                mock.uuid(),
                                self.url,
                                self.urlHash,
                                self.title,
                                self.desc,
                                self.typeName,
                                self.modifiedAt)
