'''
Created on Jun 11, 2014

@author: Maan Al Balkhi
'''
import sys
import MySQLdb

class DataTypes(object):
    UUID = "CHAR(36)"
    CHAR32 = "CHAR(32)"
    CHAR64 = "CHAR(64)"
    VCHAR32 = "VARCHAR(32)"
    VCHAR64 = "VARCHAR(64)"
    VCHAR256 = "VARCHAR(256)"
    SHA_2 = "CHAR(64)"
    DATE = "DATE"
    DATETIME = "DATETIME"
    BOOL = "TINYINT(1)"


def connect(_host, _user, _passwd, _db):
    ''' 
    create connection to DBMS.
    connection must closed by developer, use close()
    @param host: -string 
    @param user: -string
    @param passwd: -string
    @param db: -string
    '''
    try:
        conn = MySQLdb.Connect(host=_host,
                       user=_user,
                       passwd=_passwd,
                       db=_db)
    except MySQLdb.Error, e : 
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return conn

def createTable(conn, table, primaryKey, uniqueList, notNulls, forgenKeys, *order, **kwargs):
    '''
    create table.
    @param conn: connection object
    @param table: table name
    @param primaryKey: string -identify the primary key
    @param uniqueList: String list{} of unique columns
    @param notNulls: String list{} of not null columns
    @param forgenKeys: map of <column>:<<foreignTable>.<column>>   
    @param order: is a set of ordered keys 
    @param kwargs: <column>:<dataType>
    '''
    
    cursor = conn.cursor()
    
    query = "CREATE TABLE " + table + " ("
    for key in order:
        query += key + " " + kwargs[key] 
        if any(key == s for s in notNulls):
            query += " NOT NULL"
        query += ", "
    
    if primaryKey is not None:
        query += "PRIMARY KEY (" + primaryKey + "), "
    
    for key in uniqueList:
        query += "UNIQUE KEY (" + key + "), "
    
    for key, value in forgenKeys.items():
        tColumn = value.split(".") 
        query += "FOREIGN KEY (" + key + ") REFERENCES " + tColumn[0] + " (" + tColumn[1] + "), "
    
    query = query[:-2] + ")"
    print "db-api: ", query
    cursor.execute(query)
    cursor.close()

def insertToTable(conn, table, **kwargs):
    ''' 
    insert to table. 
    @param conn: connection object
    @param table: table name
    @param order: is a set of ordered keys 
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
    cursor.close()
    # TODO: should commit() be moved to a higher abstraction level?
    conn.commit()
    return cursor.rowcount

# TODO: implement select from for string search "like"
def selectFrom(conn, selectedTables, *columns, **kwargs):
    '''
    select from user
    @param conn: MySQLbd connection object
    @param selectedTables: [String] - represents selected tables
    @param *columns: <column> ordered set of columns  
    @param **kwargs: <column>:<value> includes where statement
        to select columns from multiple tables use the conventions __IN__,
        examples: column__IN__table   
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
    print query
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
    @param *tables: <tables> tables to update   
    @param **kwargs: <column>:<value> includes where statement. 
        examples: column='value' or table1.column=table2.column or table.column='value'
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
    cursor.close()
    # TODO: should commit() be moved to a higher abstraction level?
    conn.commit()
    return cursor.rowcount

def deleteFromTable(conn, table, *referencedTables,**kwargs):
    '''
    select from user
    @param conn: MySQLbd connection object
    @param table: String -table name
    @param *referencedTables: <tables> for multiple deletes example: DELETE table1, table2 FROM table1 WHERE... 
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
    cursor.close()
    # TODO: should commit() be moved to a higher abstraction level?
    conn.commit()
    return cursor.rowcount

def dropTable(conn, *tables):
    cursor = conn.cursor()
    for table in tables:
        cursor.execute("DROP TABLE IF EXISTS " + table)
