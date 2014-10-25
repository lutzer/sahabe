'''
Created on Jul 10, 2014

@author: Maan Al Balkhi
'''

from DBModelParser import Tables 
import Generator as generator

def generateMock(tables):
    content = tables.content
    mockModule ="""
import string
import random
import uuid as uid
import hashlib
import datetime


def randomText(size=64 , chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(random.randint(5, size)))

def randomEmail(size=64): 
    return randomText(size - 10) + "@sahabe.de"
    
def randomFixedLengthText(size=64, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))

def uuid():
    return str(uid.uuid4())

def timeStamp():
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(timeStamp)

def SHA2():
    return hashlib.sha256(randomText(16)).hexdigest()
    
def MD5():
    return hashlib.md5(randomText(16)).hexdigest()

class DBMock():
""" 
    init ="""
    def __init__(self):\n"""

    for table in content:
        elementName = generator.asElementName(table.name)
        className = generator.asClassName(table.name)
        dependencies = generator.getDependencies(tables, table.name)
        classArgs = ""
        for dependency in dependencies:
            classArgs += "self.%s, "%generator.asElementName(dependency)
        classArgs = classArgs.rstrip(", ")
        init +="%sself.%s = DBMock.%s(%s)\n"%(" "*8, elementName, className, classArgs) 
        
    
    classes =""
            
    for table in content:
        elementName = generator.asElementName(table.name)
        className = generator.asClassName(table.name)
        dependencies = generator.getDependencies(tables, table.name)
        classArgs = ""
        for dependency in dependencies:
            classArgs += ", %s"%generator.asElementName(dependency)
        tableClass = """
    class %s(object):
    
        def __init__(self%s):\n"""%(className, classArgs)
    
        elements = ""
        for column in table.columns:
            value = ""
            references = column.getReferenceIfExists(table)
            
            if references is not None:        
                value = "%s.%s"%(generator.asElementName(references.referToTable),
                                 generator.asElementName(references.referToColumn))
            else:    
                value = generator.randomValueByType(column)
            
            elements += "%sself.%s = %s\n"%(" "*12, generator.asElementName(column.name), value)

        tableClass += elements
        classes += tableClass
        
        print "generate Mock class for %s"%className
            
    module = open("generated/MockModule.py", "w+")    
    module.write(mockModule+
                 init+
                 classes)
    module.close()


""" don't run if its an external call """
if __name__=='__main__':
    tables = Tables()
    generateMock(tables)
