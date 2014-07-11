'''
Created on Jul 10, 2014

@author: Maan Al Balkhi
'''

class Tables():
    def __init__(self, configFile = "db_config"):
        self.content = parseTables(configFile)
        
        
    class Table():
        
        def __init__(self, name):
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
            
        def getReferencingTables(self, tables):
            referencingTables = []
            for table in tables.content:
                for fk in table.fk:
                    if fk.referToTable == self.name:
                        referencingTables.append(table)
                        break 
            
            return referencingTables
            
    class Column():
        
        def __init__(self, name, _type):
            self.name = name
            self.type =_type
            
        def getReferenceIfExists(self, table):
            for fk in table.fk:
                if self.name == fk.column:
                    return fk 
            return None
        
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
            
    def printTables(self):         
        for table in self.content:
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
            
    def getTable(self, name):
        for table in self.content:
            if table.name==name:
                return table       

    
def parseTables(configFile):
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
                table = Tables.Table(name)
                tables.append(table)
                continue
            
            if line.startswith("column__"):
                split = line.replace("column__","").split("=")
                column = Tables.Column(split[0],split[1])
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
                        reference = Tables.Reference(column, referTo[0],referTo[1])
                        tables[index].fk.append(reference)
                else:
                    columns = entries.split("+")
                    column = columns[0]
                    referTo = columns[1].split(".")
                    reference = Tables.Reference(column, referTo[0],referTo[1])
                    tables[index].fk.append(reference)
                continue
            
            if line.startswith("__END__"):
                index += 1
                continue
    return tables