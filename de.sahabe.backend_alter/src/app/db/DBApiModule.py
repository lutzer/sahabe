'''
Created on Jun 11, 2014

@author: Maan Al Balkhi
'''
import sys
import MySQLdb

CHARACTER_SET = "CHARACTER SET utf8 COLLATE utf8_unicode_ci"

class DataTypes(object):
    UUID = "CHAR(36)"
    CHAR32 = "CHAR(32)"
    CHAR64 = "CHAR(64)"
    VCHAR32 = "VARCHAR(32)"
    VCHAR64 = "VARCHAR(64)"
    VCHAR255 = "VARCHAR(255)"
    VCHAR2048 = "VARCHAR(2048)"
    VCHAR512 = "VARCHAR(512)"
    SHA_2 = "CHAR(64)"
    MD5 = "CHAR(32)"
    DATE = "DATE"
    DATETIME = "DATETIME"
    BOOL = "TINYINT(1)"
    TEXT = "TEXT"
    
class Where():
    def __init__(self, column, value):
        self.column = column
        self.value = value
        
    def like(self):
        clause = self.column + " LIKE "
        if "__IN__" in self.value: 
            value = self.value.split("__IN__")
            clause += value[1] + "." + value[0]
        else:
            clause += "'%" + self.value + "%'"
        
        return clause
     
    def equal(self):
        clause = self.column + " = "
        if "__IN__" in self.value: 
            value = self.value.split("__IN__")
            clause += value[1] + "." + value[0]
        else:
            clause += "'" + self.value + "'"
        
        return clause
        
    def ORLike(self):
        clause = "OR " + self.column + " LIKE "
        if "__IN__" in self.value: 
            value = self.value.split("__IN__")
            clause += value[1] + "." + value[0]
        else:
            clause += "'%" + self.value + "%'"
        
        return clause 

    def ANDLike(self):
        clause = "AND " + self.column + " LIKE "
        if "__IN__" in self.value: 
            value = self.value.split("__IN__")
            clause += value[1] + "." + value[0]
        else:
            clause += "'%" + self.value + "%'"
        
        return clause

    def OREqual(self):
        clause = "OR " + self.column + " = "
        if "__IN__" in self.value: 
            value = self.value.split("__IN__")
            clause += value[1] + "." + value[0]
        else:
            clause += "'" + self.value + "'"
        
        return clause 

    def ANDEqual(self):
        clause = "AND " + self.column + " = "
        if "__IN__" in self.value: 
            value = self.value.split("__IN__")
            clause += value[1] + "." + value[0]
        else:
            clause += "'" + self.value + "'"
        
        return clause
    
    def ORMatch(self):
        return "OR MATCH(%s) AGAINST('%s')"%(self.column, self.value) 
        
    def ANDMatch(self):
        return "AND MATCH(%s) AGAINST('%s')"%(self.column, self.value)    
        

def connect(host="localhost", user="sahabe", pw="sahabe", db="sahabe"):
    ''' 
    create connection to DBMS.
    connection must closed by developer, use close()
    @param host: -string 
    @param user: -string
    @param passwd: -string
    @param db: -string
    '''
    try:
        conn = MySQLdb.Connect(host=host,
                       user=user,
                       passwd=pw,
                       db=db,
                       use_unicode=False,
                       charset="utf8")
    except MySQLdb.Error, e : 
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return conn

def createTable(conn, table, primaryKey, uniqueList, notNulls, forgenKeys, searchFields, *order, **kwargs):
    '''
    create table.
    @param conn: connection object
    @param table: table name
    @param primaryKey: string -identify the primary key
    @param uniqueList: String list{} of unique columns,
        for combinations {"column1, column2"} for separated {"column1","column2"}
    @param notNulls: String list{} of not null columns
    @param forgenKeys: map of <column>:<<foreignTable>.<column>>
    @param searchFields: string array for full text searching   
    @param order: is a set of ordered keys 
    @param kwargs: <column>:<dataType>
    '''
    
    cursor = conn.cursor()
    
    query = "CREATE TABLE " + table + " ("
    for key in order:
        query += key + " " + kwargs[key] 
#         if(str(kwargs[key]).startswith("CHAR") or str(kwargs[key]).startswith("VARCHAR")):
#             query += " " + CHARACTER_SET
        if any(key == s for s in notNulls):
            query += " NOT NULL"
        query += ", "
    
    if primaryKey is not None:
        query += "PRIMARY KEY (" + primaryKey + "), "
    
    for key in uniqueList:
        #TODO: add a key name for combination column keys.
        query += "UNIQUE KEY  (" + key + "), "
    
    for key, value in forgenKeys.items():
        tColumn = value.split(".") 
        query += "FOREIGN KEY (" + key + ") REFERENCES " + tColumn[0] + " (" + tColumn[1] + ") ON DELETE CASCADE, "
    
    if searchFields is not None and searchFields !=[]:
        for searches in searchFields:
            query += "FULLTEXT (%s), "%(searches)

    query = query[:-2] + ")"
    
    print "db-api: ", query
    cursor.execute(query)
    cursor.close()

def insertToTable(conn, table, commit=True, **kwargs):
    ''' 
    insert to table. 
    @param conn: connection object
    @param table: table name
    @param commit: commit immediately after insertion   
    @param kwargs: <column>=<value>
    '''
    cursor = conn.cursor()
    
    columns = ""
    values = ""
    for key, value in kwargs.items():
        columns += key + " , "
        values += "'" + value + "' , "
    query = "INSERT INTO " + table + " (" + columns[:-2] + ") VALUES (" + values[:-2] + ")" 
    cursor.execute(query)
    
    if commit:
        conn.commit()
    
    cursor.close()
    return cursor.rowcount


def selectFormWhereClause(conn, fromTables, columns, *where):
    cursor = conn.cursor()
    
    query = "SELECT "
    query += ", ".join(columns)
    query += " FROM "
    query += ", ".join(fromTables)
    if where != [] and where is not None:
        query += " WHERE " + " ".join(where) 
    
    cursor.execute(query)
    
    rows = []
    while (1):
        row = cursor.fetchone()
        if row == None:
            break
        rows.append(row)
    cursor.close()
    return rows


# TODO: implement select from for string search "like"
def selectFrom(conn, selectedTables, *columns, **kwargs):
    '''
    select from user
    @param conn: MySQLdb connection object
    @param selectedTables: [String] - represents selected tables
    @param *columns: <column> ordered set of columns  
    @param **kwargs: <column>:<value> includes where statement
        to select columns from multiple tables use the conventions __IN__,
        example: column__IN__table   
    '''
    cursor = conn.cursor()
    queryColumns = ""    
    for column in columns:
            queryColumns += column + ", "
    
    tables = ""
    for table in selectedTables:
        tables += table + ", "
    tables = tables[:-2]
    
    where = ""
    if kwargs != {}:
        where = " WHERE "
        for tColumn, val in kwargs.items():
            if "__IN__" in tColumn:
                tCol = tColumn.split("__IN__")
                tColumn = tCol[1] + "." + tCol[0]
            if "__IN__" in val:
                tVal = val.split("__IN__")
                val = tVal[1] + "." + tVal[0]
                where += tColumn + " = " + val + " AND "
            else:
                where += tColumn + " = '" + val + "' AND "    
        where = where[:-4]
    
    query = "SELECT " + queryColumns[:-2] + " FROM " + tables + where  
    cursor.execute(query)
    
    rows = []
    while (1):
        row = cursor.fetchone()
        if row == None:
            break
        rows.append(row)
    cursor.close()
    return rows

def updateInTable(conn, colValueMap, *inTables, **kwargs):
    '''
    select from user
    @param conn: MySQLbd connection object
    @param colValueMap: {column:value}. SQL query: ..SET column='value' WHERE.... 
    @param *inTables: <tables> tables to update   
    @param **kwargs: <column>:<value> includes where statement. 
        SQL query: column='value' or table1.column=table2.column or table.column='value'
    '''
    cursor = conn.cursor()
    
    columnValues = ""
    for key, value in colValueMap.items():
        columnValues += key + " = '" + value + "', "
    columnValues = columnValues[:-2]
    
    tables = ""
    for table in inTables:
        tables += table + ", "
    tables = tables[:-2]
    
    where = ""
    if kwargs is not None:
        where = " WHERE "
        for col, val in kwargs.items():
            where += col + "= '" + val + "' AND "
        where = where[:-4]   
    
    query = "UPDATE " + tables + " SET " + columnValues + where
    cursor.execute(query)
    # TODO: should commit() be moved to a higher abstraction level?
    conn.commit()
    cursor.close()
    return cursor.rowcount

def deleteFromTable(conn, table, *referencedTables,**kwargs):
    '''
    select from user
    @param conn: MySQLbd connection object
    @param table: String -table name
    @param *referencedTables: <tables> for multiple deletes. SQL query: DELETE table1, table2 FROM table1 WHERE... 
    @param **kwargs: <column>:<value> includes where statement
        examples: column='value' or table1.column=table2.column or table.column='value'
    '''
    cursor = conn.cursor()
    
    tables = ""
    for tbl in referencedTables:
        tables += tbl + ", "
    tables = tables[:-2]
    
    where = ""
    if kwargs is not None:
        where = " WHERE "
        for col, val in kwargs.items():
            where += col + "= '" + val + "' AND "
        where = where[:-4]   
    
    query = "DELETE " + tables +" FROM " + table + where
    cursor.execute(query)
    # TODO: should commit() be moved to a higher abstraction level?
    conn.commit()
    cursor.close()
    return cursor.rowcount

def dropTable(conn, *tables):
    cursor = conn.cursor()
    for table in tables:
        cursor.execute("DROP TABLE IF EXISTS " + table)
    cursor.close()
