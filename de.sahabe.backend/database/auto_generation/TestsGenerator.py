'''
Created on Jul 10, 2014

@author: Maan Al Balkhi
'''

from DBModelParser import Tables 
import Generator as generator

def generateAssertEquals(table, notSelfElement, indent, prefix = ""):
    asserts = ""
    index = 0
    for column in table.columns:
        refer = column.getReferenceIfExists(table)
        name = ""
        if refer is not None:
            name ="self.%s.%s"%(generator.asElementName(refer.referToTable), 
                                generator.asElementName(refer.referToColumn))
        else:
            if prefix == "":
                if  column.name != notSelfElement:
                    name = "self.%s"%generator.asElementName(column.name)
                else:
                    name = "_%s"%generator.asElementName(column.name)
            else:
                if  column.name != notSelfElement:
                    name = "%s.%s"%(prefix, generator.asElementName(column.name))
                
        asserts += "%sself.assertEqual(%s, str(rows[0][%s]))\n"%(" "*8, name, index)
        index += 1 
    return asserts    

def generateUpdateTest(table, testIndent):
    indent = testIndent + 4
    updates = ""
    for column in table.columns:
        
        
        fk = column.getReferenceIfExists(table)
        
        if fk is not None:
            """ UPDATE TO EXISTING """
            updates += "%sdef\ttestUpdateToExisting%s(self):\n"%(" " *testIndent,generator.asClassName(column.name))
            elementName = generator.asElementName(column.name)
            updates += generator.insertToDB(table, indent) +"\n"
            
            tableElement = generator.asElementName(table.name)
            updates += "%s%s = self.%s\n"%(" "*indent, tableElement, tableElement)
            updates += "%sself.__initDependencies()\n"%(" "*indent)
            identifier = table.columns[0].name
            updates += """%sdb.updateInTable(self.conn, {"%s":self.%s}, "%s", %s=%s.%s)\n"""%(" "*indent,
                                            column.name, elementName, table.name, 
                                            identifier,
                                            tableElement,
                                            generator.asElementName(identifier))

            updates += """%srows = db.selectFrom(self.conn, {"%s"}, "*", %s=%s.%s)\n\n"""%(" "*indent,
                                            table.name, 
                                            identifier,
                                            tableElement,
                                            generator.asElementName(identifier))
            
            updates += generateAssertEquals(table, column.name, indent, tableElement)+"\n"
            
            """ UPDATE TO NONE EXISTING """
            updates += "%sdef\ttestUpdateToNonExisting%s(self):\n"%(" " *testIndent,generator.asClassName(column.name))
            elementName = generator.asElementName(column.name)
            updates += generator.insertToDB(table, indent) +"\n"
            
            tableElement = generator.asElementName(table.name)
            updates += "%s_%s = mock.%s\n"%(" "*indent, elementName, generator.randomValueByType(column))
            identifier = table.columns[0].name
            
            updates += """%sself.assertRaisesRegexp(IntegrityError, "foreign key constraint fails",db.updateInTable,
                                                   self.conn,
                                                   {"%s":_%s},
                                                   "%s",
                                                   %s=self.%s)\n"""%(" "*indent, column.name,
                                                                     elementName, table.name,
                                                                     identifier, 
                                                                     generator.asElementName(identifier)) 

        else:
            updates += "%sdef\ttestUpdate%s(self):\n"%(" " *testIndent,generator.asClassName(column.name))
            elementName = generator.asElementName(column.name)
            updates += generator.insertToDB(table, indent) +"\n"
            
            updates += "%s_%s = mock.%s\n"%(" "*indent, elementName, generator.randomValueByType(column))
            identifier = table.columns[0].name
            updates += """%sdb.updateInTable(self.conn, {"%s":_%s}, "%s", %s=self.%s)\n"""%(" "*indent,
                                            column.name, elementName, table.name, 
                                            identifier,
                                            generator.asElementName(identifier))
            whereValue = ""
            if column.name == identifier:
                whereValue = "_" + elementName
            else:
                whereValue = "self." + generator.asElementName(identifier)
            updates += """%srows = db.selectFrom(self.conn, {"%s"}, "*", %s=%s)\n\n"""%(" "*indent,
                                            table.name, 
                                            identifier,
                                            whereValue)
            
            updates += generateAssertEquals(table, column.name, indent)+"\n"
            
    return updates
        

def generateDropTest(tables, table, testIndent):
    indent = testIndent + 4
    identifier = table.columns[0].name
    idElement = generator.asElementName(identifier)
    drop = "%sdef\ttestDrop%s(self):\n"%(" " *testIndent, generator.asClassName(table.name))
    drop += generator.insertToDB(table, indent)
    drop += """%sdb.deleteFromTable(self.conn, "%s", %s=self.%s)\n"""%(" "*indent,
                                                                     table.name,
                                                                     identifier,
                                                                     idElement)
    drop += """%srows = db.selectFrom(self.conn, {"%s"}, "*", %s=self.%s)\n"""%(" "*indent,
                                            table.name, 
                                            identifier,
                                            idElement)
    drop += "%sself.assertEqual(rows, [])\n\n"%(" "*indent)
    
    referencingTables = table.getReferencingTables(tables)

    for refTable in referencingTables:
        drop += "%sdef\ttestDrop%sBy%s(self):\n"%(" " *testIndent,
                                                 generator.asClassName(refTable.name),
                                                 generator.asClassName(table.name))
        
        drop += generator.insertToDB(table, indent)
        drop += generator.insertToDB(refTable, indent, generator.asElementName(refTable.name))
        drop += """%sdb.deleteFromTable(self.conn, "%s", %s=self.%s)\n"""%(" "*indent,
                                                                         table.name,
                                                                         identifier,
                                                                         idElement)
        drop += """%srows = db.selectFrom(self.conn, {"%s"}, "*", %s=self.%s.%s)\n"""%(" "*indent,
                                            refTable.name, 
                                            refTable.columns[0].name,
                                            generator.asElementName(refTable.name),
                                            generator.asElementName(refTable.columns[0].name))
        drop += "%sself.assertEqual(rows, [])\n\n"%(" "*indent)    
    
    
    return drop


def generateDataTypeTest(table, testIndent):
    indent = testIndent + 4
    tests = ""
    for column in table.columns:
        tests = "%sdef\ttestInsertInvalid%s(self):\n"%(" " *testIndent,
                                                     generator.asClassName(column.name)) 
        tests += "%s_%s = %s"%(indent, 
                               generator.asElementName(column.name),
                               generator.invalidValueByType(column))
        tests += "%sself.assertRaisesRegexp(DataError, self.insert%s ,\n"%(indent,
                                                                           generator.asClassName(table.name))

        
        


    return tests


def generateTest(tables):
    content = tables.content   
    for table in content:
        tableName = generator.asClassName(table.name)
        moduleName = tableName + ".py"
        
        imports = """
import Tables as tables
import MockModule as mock
import impl.DBApiModule as db
from _mysql_exceptions import DataError, OperationalError, IntegrityError
        
"""
        
        classDef="""
class %s(tables.Tables):
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
        
        """%(tableName)    
        
            
        dependencies="""
    def __initDependencies(self):
        self.initDBMockContents()\n%s%s"""%(generator.attributes(table, 8),
                                            generator.insertReferences(tables, table, 8))
        
        setUp ="""
    def setUp(self):
        self.connect()
        self.__initDependencies()
        """    
        
        tearDown ="""
    def tearDown(self):
        self.conn.close()
        """

        select ="""
        rows = db.selectFrom(self.conn, {"%s"}, "*", id=self.%s)
        """%(table.name, table.columns[0].name)
        
        insertion ="""
    ''' INSERTION TESTS '''
    
    def testInsertion(self):\n%s%s\n%s
        """%(generator.insertToDB(table, 8), select, generateAssertEquals(table, "", 8))
        
        updates ="""
    ''' UPDATE TESTS '''\n\n%s"""%(generateUpdateTest(table, 4))
        
        
        drop ="""
    ''' DROP TESTS '''\n\n%s"""%(generateDropTest(tables, table, 4))
        
        dataTypes ="""
    ''' DATA TYPE TESTS '''\n\n%s"""%(generateDataTypeTest(table, 4))
        
        testModule = (imports + classDef + dependencies + setUp + tearDown + insertion + updates +
                     drop + dataTypes)
        module = open("generated/"+moduleName, "w+")    
        module.write(testModule)
        module.close()
        print "test for %s were generated"%tableName


""" don't run if its an external call """
if __name__=='__main__':
    tables = Tables()
    generateTest(tables)
