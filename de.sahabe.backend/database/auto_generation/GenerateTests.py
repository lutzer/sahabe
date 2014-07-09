'''
Created on Jul 8, 2014

@author: Maan Al Balkhi
'''

import re

class Table():
    
    def __init__(self, name ):
        '''
        @param name: string -table name
        @param columns: [Column] - columns 
        @param pk: [string] - primary key
        @param unique: [[string]] - unique constrains
        @param notNull: [string] - not null constrains
        @param fk: [References] - foreign key constrains
        '''
        self.name=name
        self.columns = []
        self.pk = []
        self.unique=[]
        self.notNull= []
        self.fk = []
        
class Column():
    
    def __init__(self, name, _type):
        self.name = name
        self.type =_type
        
class Reference():

    def __init__(self, column, referToTable, referToColumn):
        '''
        @param column: string - column name
        @param referToTable: string 
        @param referToColumn: string
        '''
        self.column = column
        self.referToTable = referToTable
        self.referToColumn = referToColumn
        
def printTables(tables):         
    for table in tables:
        print "--------"+table.name+"--------"
        print " ---COLUMN---"
        for column in table.columns:
            print column.name  
        print " ---PK---"
        for pk in table.pk:
            print pk +  " "
        print " ---UNIQUE---"
        for unique in table.unique:
            entry = ""
            for column in unique:
                entry = entry + " AND " + column
            entry = entry.lstrip(" AND ")
            print entry   
        print " ---NOT NULL---"
        for nn in table.notNull:
            print nn +" "
        print " ---FK---"
        for fk in table.fk:
            print "column "+fk.column +" to table " +fk.referToTable+" to column "+fk.referToColumn
         
        print
        
def getTable(tables, name):
    for table in tables:
        if table.name==name:
            return table       

def parseTables(configFile = "db_config"):
    tables = []
    with open(configFile, "r") as config:
        index = 0
        for line in config:
            '''
            strip whitespaces
            '''
            line = line.replace(" ", "").replace("\t","").replace("\r","").replace("\n","")

            if line.startswith("__START__"):    
                split = next(config).replace(" ","").replace("\r","").replace("\t","").replace("\n","").split("=")
                if split[0]!="name":
                    raise Exception("tag name expected")
                name = split[1]
                table = Table(name)
                tables.append(table)
                continue
            
            if line.startswith("column__"):
                split = line.replace("column__","").split("=")
                column = Column(split[0],split[1])
                tables[index].columns.append(column)
                continue
            
            if line.startswith("primary_key"):
                columns = line.replace("primary_key=","")
                if "," in columns:
                    columns = columns.split(",")
                    for column in columns:
                        tables[index].pk.append(column)
                else:
                    tables[index].pk.append(columns)
                continue
            
            if line.startswith("unique_key"):
                entries = line.replace("unique_key=","")
                if "," in entries:
                    entries = entries.split(",")
                    for entry in entries:
                        columns = []
                    
                        if "AND" in entry:
                            entryColumns = entry.split("AND") 
                            for column in entryColumns:
                                columns.append(column)
                        else:
                            columns.append(entry)
                        
                        tables[index].unique.append(columns)
                else:
                    tables[index].unique.append(entries)
                continue
            
            if line.startswith("not_null"):
                columns = line.replace("not_null=","")
                if "," in columns:
                    columns = columns.split(",") 
                    for column in columns:
                        tables[index].notNull.append(column)
                else:
                    tables[index].notNull.append(columns)
                continue
            
            if line.startswith("foreign_key"):
                entries = line.replace("foreign_key=","")
                if "," in entries:
                    split = entries.split(",")
                    for entry in split:
                        columns = entry.split("+")
                        column = columns[0]
                        referTo = columns[1].split(".")
                        reference = Reference(column, referTo[0],referTo[1])
                        tables[index].fk.append(reference)
                else:
                    columns = entries.split("+")
                    column = columns[0]
                    referTo = columns[1].split(".")
                    reference = Reference(column, referTo[0],referTo[1])
                    tables[index].fk.append(reference)
                continue
            
            if line.startswith("__END__"):
                index += 1
                continue
    return tables

def references(tables, table, indent):
        dependencies=""
        for fk in table.fk:
            entry= "%sself.insert%s("%(" "*indent, fk.referToTable.title())
            referTo = getTable(tables, fk.referToTable)
            neededTables = references(tables, referTo, 8)
            if neededTables not in dependencies:  
                dependencies += neededTables 
            for column in referTo.columns:
                entry += "self.%s.%s, "%(referTo.name, column.name)
            dependencies += entry.rstrip(", ")+")\n"
        return dependencies

def attributes(table, indent):
    attributes=""
    for column in table.columns:
        name = column.name
        if "_" in name:
            split = name.split("_")
            name = split[0]+split[1].title() 
        attributes += "%sself.%s = self.%s.%s\n"%(" "*indent, name, table.name, name)
        
    return attributes


tables = parseTables()

def asElementName(name):
    split = name.split("_")
    element = split[0]
    for i in range(1,len(split)):
        element += split[i].title() 
    return element
        
def asClassName(name):
    return name.title().replace("_", "")

def getDependencies(tables, name):
    dependencies =[]
    table = getTable(tables, name)
    for fk in table.fk:
        dependencies.append(fk.referToTable)
    return dependencies

def extractNumber(_str):    
        result = ""
        split = list(_str)
        for s in split:
            if s.isdigit():
                result += s
        return int(result)
    
def generateTest(tables):    
    for table in tables:
        tableName = asClassName(table.name)
        moduleName = tableName + ".py"
        
        imports = """
    import test.Tables as tables
    import test.MockModule as mock
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
            self.initDBMockContents()\n%s%s"""%(attributes(table, 8), references(tables, table, 8))
        
        setUp ="""
        def setUp(self):
            self.connect()
            self.__initDependencies()
        """    
        
        tearDown="""
        def tearDown(self):
            self.conn.close()
        """
   
        module = open(moduleName, "w+")    
        module.write(imports+
                     classDef+
                     dependencies+
                     setUp+
                     tearDown)
        module.close()


def generateMock(tables):
    
    mockModule ="""
import string
import random
import uuid as uid
import hashlib
import datetime


def randomText(size=64 , chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(random.randint(5, size)))

def randomEmail(size=64): 
    return randomText(size - 10) + "@sahabe.de"
    
def randomFixedLengthText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def uuid():
    return str(uid.uuid4())

def timeStamp():
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(timeStamp)


class DBMock():
""" 
    init ="""
    def __init__(self):\n"""

    for table in tables:
        elementName = asElementName(table.name)
        className = asClassName(table.name)
        dependencies = getDependencies(tables, table.name)
        classArgs = ""
        for dependency in dependencies:
            classArgs += "self.%s, "%asElementName(dependency)
        classArgs = classArgs.rstrip(", ")
        init +="%sself.%s = DBMock.%s(%s)\n"%(" "*8, elementName, className, classArgs) 
        
    
    classes =""
            
    for table in tables:
        elementName = asElementName(table.name)
        className = asClassName(table.name)
        dependencies = getDependencies(tables, table.name)
        classArgs = ""
        for dependency in dependencies:
            classArgs += ", %s"%asElementName(dependency)
        tableClass = """
    class %s(object):
    
        def __init__(self%s):\n"""%(className, classArgs)
    
        elements = ""
        for column in table.columns:
            value = ""
            columnReference = None
            
            for fk in table.fk:
                if fk.column == column.name:
                    columnReference = fk
                    break
                    
            if columnReference is not None:        
                value = "%s.%s"%(asElementName(fk.referToTable), asElementName(fk.referToColumn))
                
            elif column.type == "UUID":
                value = "uuid()"
                
            elif column.type.startswith("VCHAR"):
                length = re.search("[0-9]+", column.type).group(0)
                value = "randomText(%s)"%(length)
                
            elif column.type.startswith("CHAR"):
                length = re.search("[0-9]+", column.type).group(0)
                value = "randomText(%s)"%(length)
                
            elif column.type == "TEXT":
                value = "randomText(2048)"
                
            elif column.type == "SHA_2":
                value = "hashlib.sha256(randomText(16)).hexdigest()"
            
            elif column.type == "MD5":
                value = "hashlib.md5(randomText(16)).hexdigest()"
            
            elif column.type == "DATETIME":
                value = "timeStamp()"
            
            elif column.type == "BOOl":
                value = "'0'"
            
            elements += "%sself.%s = %s\n"%(" "*12, asElementName(column.name), value)
        
        tableClass += elements
        classes += tableClass
            
    module = open("generated_MockModule.py", "w+")    
    module.write(mockModule+
                 init+
                 classes)
    module.close()
    
generateMock(tables)        
