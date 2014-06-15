'''
Created on Jun 15, 2014

@author: maan al balkhi
'''

import Tables
import test.MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError


class Link(Tables.Tables):
    """
    - Test: insertion and fetching data from/to table
    - Test: references.
    - Test: inserting invalid date
    - Test: NOT NULLS constrains
    - Test: UNIQUE constrains
    """
    
    def __initDependencies(self):
        self.initDBMockContents()
        self.id = self.link.id
        self.userId = self.link.userId
        self.catId = self.link.catId
        self.url = self.link.url
        self.name = self.link.name
        self.desc = self.link.description
        self.date = self.link.createDate
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertCategory(self.cat.id, self.cat.userId, self.cat.name)
    
    def setUp(self):
        self.connect()
        self.initDBMockContents()
        self.id = self.link.id
        self.userId = self.link.userId
        self.catId = self.link.catId
        self.url = self.link.url
        self.name = self.link.name
        self.desc = self.link.description
        self.date = self.link.createDate
        self.insertUser(self.user.id, self.user.name, self.user.email)
        self.insertCategory(self.cat.id, self.cat.userId, self.cat.name)
        
    def tearDown(self):
        self.conn.close()
    
    def testInsertion(self):
        self.insertLink(self.id, self.userId, self.catId, self.url, self.name,
                        self.desc, self.date)
        
        rows = db.selectFrom(self.conn, "link", "*", id=self.id)
        
        self.assertEqual(self.id, rows[0][0])
        self.assertEqual(self.user.id, rows[0][1])
        self.assertEqual(self.cat.id, rows[0][2])
        self.assertEqual(self.url, rows[0][3])
        self.assertEqual(self.name, rows[0][4])
        self.assertEqual(self.desc, rows[0][5])
        self.assertEqual(self.date, str(rows[0][6]))
        
        
    
    
    """ DATA TYPE TESTS """

    def testInsertInvalidId(self):
        self.assertRaises(DataError, self.insertLink ,
                         self.id + "e", self.userId, self.catId, self.url,
                         self.name, self.desc, self.date)
        """ insert too short """
        # FIXME: what's about UUID length constrains? 
        """
        self.assertRaises(DataError, self.insertLink ,
                         self.id[:-13], self.name, self.email)
        """
        
    def testInsertInvalidUserId(self):
        self.assertRaises(DataError, self.insertLink,
                         self.id,
                         mock.uuid() + "e",
                         self.catId,
                         self.url,
                         self.name,
                         self.desc,
                         self.date)
    
    def testInsertInvalidCategoryId(self):
        self.assertRaises(DataError, self.insertLink,
                         self.id,
                         self.userId,
                         mock.uuid() + "e",
                         self.url,
                         self.name,
                         self.desc,
                         self.date)

    def testInsertInvalidUrl(self):
        url = mock.randomText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaises(DataError, self.insertLink,
                         self.id,
                         self.userId,
                         self.catId,
                         url,
                         self.name,
                         self.desc,
                         self.date)
        
    def testInsertInvalidName(self):
        name = mock.randomText(self.extractNumber(db.DataTypes.VCHAR64) + 2)
        self.assertRaises(DataError, self.insertLink,
                         self.id,
                         self.userId,
                         self.catId,
                         self.url,
                         name,
                         self.desc,
                         self.date)
        
    def testInsertInvaliddescription(self):
        desc = mock.randomText(self.extractNumber(db.DataTypes.VCHAR255) + 2)
        self.assertRaises(DataError, self.insertLink,
                         self.id,
                         self.userId,
                         self.catId,
                         self.url,
                         self.name,
                         desc,
                         self.date)
        
    def testInsertInvalidCreateDate(self):
        date = mock.randomText(64)
        self.assertRaises(OperationalError, self.insertLink,
                         self.id,
                         self.userId,
                         self.catId,
                         self.url,
                         self.name,
                         self.desc,
                         date)
       
    
    """ NULL CONSTRAINS TESTS """ 
        
    def testInsertNoId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "link",
                          user_id=self.userId,
                          category_id=self.catId,
                          url=self.url,
                          name=self.name,
                          description=self.desc,
                          create_date=self.date)
        
    def testInsertNoUserId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "link",
                          id=self.id,
                          category_id=self.catId,
                          url=self.url,
                          name=self.name,
                          description=self.desc,
                          create_date=self.date)
                
    def testInsertNoCategoryId(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          url=self.url,
                          name=self.name,
                          description=self.desc,
                          create_date=self.date)

    def testInsertNoUrl(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          category_id=self.catId,
                          name=self.name,
                          description=self.desc,
                          create_date=self.date)

    def testInsertNoName(self):
        db.insertToTable(self.conn, "link",
                         id=self.id,
                         user_id=self.userId,
                         category_id=self.catId,
                         url=self.url,
                         description=self.desc,
                         create_date=self.date)
    
    def testInsertNoDescription(self):
        db.insertToTable(self.conn, "link",
                         id=self.id,
                         user_id=self.userId,
                         category_id=self.catId,
                         url=self.url,
                         name=self.name,
                         create_date=self.date)
        
    def testInsertNoCreateDate(self):
        self.assertRaises(OperationalError, db.insertToTable , self.conn, "link",
                          id=self.id,
                          user_id=self.userId,
                          category_id=self.catId,
                          url=self.url,
                          name=self.name,
                          description=self.desc)


    """ UNIQUE CONSTRAINS TESTS """    
    # FIXME: what's about UNIQUE constrains?
        
    def testInsertDublicateId(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        _id = self.id
        self.__initDependencies()
        self.assertRaises(IntegrityError, self.insertLink,
                          _id,
                          self.userId,
                          self.catId,
                          self.url,
                          self.name,
                          self.desc,
                          self.date)
        
    def testInsertDublicateUserId(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        userId = self.userId
        self.__initDependencies()
        self.assertRaises(IntegrityError, self.insertLink,
                          self.id,
                          userId,
                          self.catId,
                          self.url,
                          self.name,
                          self.desc,
                          self.date)
        
    def testInsertDublicateCatId(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        catId = self.catId
        self.__initDependencies()
        self.assertRaises(IntegrityError, self.insertLink,
                          self.id,
                          self.userId,
                          catId,
                          self.url,
                          self.name,
                          self.desc,
                          self.date)
        
    def testInsertDublicateUrl(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        url = self.url
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.catId,
                        url,
                        self.name,
                        self.desc,
                        self.date)
    
    def testInsertDublicateName(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        name = self.name
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.catId,
                        self.url,
                        name,
                        self.desc,
                        self.date)
        
    def testInsertDublicateDescription(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        desc = self.desc
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.catId,
                        self.url,
                        self.name,
                        desc,
                        self.date)
        
    def testInsertDublicateCreateDate(self):
        self.insertLink(self.id, self.userId, self.catId, self.url,
                        self.name, self.desc, self.date)
        date = self.date
        self.__initDependencies()
        self.insertLink(self.id,
                        self.userId,
                        self.catId,
                        self.url,
                        self.name,
                        self.desc,
                        date)
