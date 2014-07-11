'''
Created on Jul 8, 2014

@author: Maan Al Balkhi
'''

from DBModelParser import Tables 
import re
import TestsGenerator
import MockGenerator


def randomValueByType(column):
    if column.type == "UUID":
        return "uuid()"
        
    elif column.type.startswith("VCHAR"):
        length = re.search("[0-9]+", column.type).group(0)
        return "randomText(%s)"%(length)
        
    elif column.type.startswith("CHAR"):
        length = re.search("[0-9]+", column.type).group(0)
        return "randomText(%s)"%(length)
        
    elif column.type == "TEXT":
        return "randomText(2048)"
        
    elif column.type == "SHA_2":
        return "SHA2()"
    
    elif column.type == "MD5":
        return "MD5()"
    
    elif column.type == "DATETIME":
        return "timeStamp()"
    
    elif column.type == "BOOl":
        return "random.choice('01')"
    
def invalidValueByType(column, increaseValue = True, by = 5 ):
    
    if column.type == "UUID":
        return "uuid() + randomText(%s)"%by if increaseValue else "uuid()[:-%s]"%by
        
    elif column.type.startswith("VCHAR"):
        length = re.search("[0-9]+", column.type).group(0)
        length = length + by if increaseValue else length - by
        return "randomText(%s)"%(length) 
        
    elif column.type.startswith("CHAR"):
        length = re.search("[0-9]+", column.type).group(0)
        length = length + by if increaseValue else length - by
        return "randomText(%s)"%(length)
        
    elif column.type == "TEXT":
        length = 2048
        length = length + by if increaseValue else length - by
        return "randomText(%s)"%(length)
        
    elif column.type == "SHA_2":
        return "SHA2() + randomText(%s)"%by if increaseValue else "SHA2()[:-%s]"%by
    
    elif column.type == "MD5":
        return "MD5() + randomText(%s)"%by if increaseValue else "MD5()[:-%s]"%by
    
    elif column.type == "DATETIME":
        return "timeStamp() + randomText(%s)"%by if increaseValue else "timeStamp()[:-%s]"%by
        
    elif column.type == "BOOl":
        return "random.choice(' \n\t\r/@[]{}\%&<>=-+*|_';:.ABCDEFGabcdefg')"
    
    else:
        raise Exception("type not found")    

def insertReferences(tables, table, indent):
        dependencies=""
        for fk in table.fk:
            entry= "%sself.insert%s("%(" "*indent, asClassName(fk.referToTable))
            referTo = tables.getTable(fk.referToTable)
            neededTables = insertReferences(tables, referTo, indent)
            if neededTables not in dependencies:  
                dependencies += neededTables 
            for column in referTo.columns:
                entry += "self.%s.%s, "%(asElementName(referTo.name), asElementName(column.name))
            dependencies += entry.rstrip(", ")+")\n"
        return dependencies

def insertToDB(table, indent, prefix = ""):
    results = "%sself.insert%s("%(" "*indent, asClassName(table.name))
    for column in table.columns:
        if prefix == "":
            results += "self.%s, "%(asElementName(column.name))
        else:
            results += "self.%s.%s, "%(prefix, asElementName(column.name))
    results = results.rstrip(", ")+")\n"    
    return results

def attributes(table, indent):
    attributes=""
    for column in table.columns:
        name = column.name
        if "_" in name:
            split = name.split("_")
            name = split[0]+split[1].title() 
        attributes += "%sself.%s = self.%s.%s\n"%(" "*indent, name, asElementName(table.name), name)
        
    return attributes

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
    table = tables.getTable(name)
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
    
""" don't run if its an external call """
if __name__=='__main__':    
    tables = Tables()
    MockGenerator.generateMock(tables)        
    TestsGenerator.generateTest(tables)