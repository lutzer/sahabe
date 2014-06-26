'''
Created on Jun 15, 2014

@author: Maan Al Balkhi
'''

import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class Link(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid modifiedAt
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    - Test: FOREIGN KEY CONSTRAINS
    """
    
    def __initDependencies(self):
        self.initDBMockContents()
        self.id = self.link.id
        self.userId = self.link.userId
        self.url = self.link.url
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
    
    def testInsertion(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc, self.typeName ,self.modifiedAt)
        
        rows = db.selectFrom(self.conn, "link", "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.url, rows[0][2])
        self.assertEqual(self.title, rows[0][3])
        self.assertEqual(self.desc, rows[0][4])
        self.assertEqual(self.typeName, rows[0][5])
        self.assertEqual(self.modifiedAt, str(rows[0][6]))
        
        
    
    
    """ DATA TYPE TESTS """

    def testInsertInvalidId(self):
        self.assertRaises(DataError, self.insertLink ,
                         self.id + "e", self.userId, self.url, self.title,
                         self.desc, self.typeName, self.modifiedAt)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertLink ,
                         self.id[:-13], self.title, self.email)
        """
        
    def testInsertInvalidUserId(self):
        self.assertRaisesRegexp(DataError, "Data too long" ,self.insertLink,
                         self.id,
                         mock.uuid() + "e",
                         self.url,
                         self.title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)

    def testInsertInvalidUrl(self):
        url = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         url,
                         self.title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertInvalidTitle(self):
        title = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertInvaliddescription(self):
        desc = mock.randomText(self.extractNumber(db.DataTypes.VCHAR256) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.title,
                         desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertInvalidTypeName(self):
        typeName = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaisesRegexp(DataError, "Data too long", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.title,
                         self.desc,
                         typeName,
                         self.modifiedAt)
        
    def testInsertInvalidModifiedAt(self):
        self.assertRaisesRegexp(OperationalError, "Incorrect datetime value", self.insertLink,
                         self.id,
                         self.userId,
                         self.url,
                         self.title,
                         self.desc,
                         self.typeName,
                         mock.randomText(64))
       
    
    """ NULL CONSTRAINS TESTS """ 
        
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
                         description=self.desc,
                         type_name=self.typeName,
                         modified_at=self.modifiedAt)
    
    def testInsertNoDescription(self):
        db.insertToTable(self.conn, "link",
                         id=self.id,
                         user_id=self.userId,
                         url=self.url,
                         title=self.title,
                         type_name=self.typeName,
                         modified_at=self.modifiedAt)
        
    
    def testInsertNoTypeName(self):
        db.insertToTable(self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          url=self.url,
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
                          title=self.title,
                          description=self.desc,
                          type_name=self.typeName)


    """ UNIQUE CONSTRAINS TESTS """    

    def testInsertDublicateId(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc,  self.typeName, self.modifiedAt)
        _id = self.id
        self.__initDependencies()
        self.assertRaisesRegexp(IntegrityError, "Duplicate entry", self.insertLink,
                          _id,
                          self.userId,
                          self.url,
                          self.title,
                          self.desc,
                          self.typeName,
                          self.modifiedAt)
        
    def testInsertDublicateUserId(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc,  self.typeName, self.modifiedAt)
        userId = self.userId
        self.__initDependencies()
        self.insertLink(self.id,
                         userId,
                         self.url,
                         self.title,
                         self.desc,
                         self.typeName,
                         self.modifiedAt)
        
    def testInsertDublicateUrl(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc,  self.typeName, self.modifiedAt)
        url = self.url
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        url,
                        self.title,
                        self.desc,
                        self.typeName,
                        self.modifiedAt)
    
    def testInsertDublicateTitle(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc,  self.typeName, self.modifiedAt)
        title = self.title
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.url,
                        title,
                        self.desc,
                        self.typeName,
                        self.modifiedAt)
        
    def testInsertDublicateDescription(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc,  self.typeName, self.modifiedAt)
        desc = self.desc
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.url,
                        self.title,
                        desc,
                        self.typeName,
                        self.modifiedAt)
        
    def testInsertDublicateModifiedAt(self):
        self.insertLink(self.id, self.userId, self.url, self.title,
                        self.desc,  self.typeName, self.modifiedAt)
        modifiedAt = self.modifiedAt
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.url,
                        self.title,
                        self.desc,
                        self.typeName,
                        modifiedAt)
        
        
    """ FOREIGN KEY CONSTRAINS TESTS """
    
    def testInsertNonExistingUserId(self):
        self.assertRaisesRegexp(IntegrityError, "foreign key constraint fails", self.insertLink,
                                self.id,
                                mock.uuid(),
                                self.url,
                                self.title,
                                self.desc,
                                self.typeName,
                                self.modifiedAt)
        
    #TODO: implement update user.id tests
    #TODO: implement drop user.id test
