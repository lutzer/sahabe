'''
Created on Jun 11, 2014

@author: maan al balkhi
'''
import sys
import MySQLdb

def connect(_host, _user, _passwd, _db):
    ''' 
    create connection to DBMS.
    connection must closed by developer, use close()
    @param host:
    @param user: 
    @param passwd: 
    @param db:  
    '''
    try:
        conn = MySQLdb.Connect(host=_host,
                       user=_user,
                       passwd=_passwd,
                       db=_db)
    except MySQLdb.Error, e : 
        print "Error %d: %s % (e.args[0], e.args[1])"
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
    
    cursor.execute(query)
    cursor.close()
    
def insertToTable(conn, table, *order, **kwargs):
    ''' 
    insert to table. 
    @param conn: connection object
    @param table: table name
    @param order: is a set of ordered keys 
    @param kwargs: <column>=<dataType>
    '''
    cursor = conn.cursor()
    
    columns = ""
    values = ""
    for key in order:
        columns += key + " , "
        values += "'" + kwargs[key] + "' , "
    query = "INSERT INTO " + table + " (" + columns[:-2] + ") VALUES (" + values[:-2] + ")" 
    
    cursor.execute(""" query """)
    cursor.close()
    # TODO: should commit() be moved to a higher abstraction level?
    conn.commit()
    return cursor.rowcount

def selectFrom(conn, table, *columns):
    '''
    select from user
    @param conn: MySQLbd connection object
    @param table: String -table name
    @param order: a set of ordered String keys 
    @param kwargs: <column>=<dataType>
    '''
    cursor = conn.cursor()
    query_columns = ""    
    for column in columns:
            query_columns += column + ", "
    query = "SELECT " + query_columns[:-2] + " FROM " + table
    cursor.execute(query)
    
    rows = []
    while (1):
        row = cursor.fetchone()
        if row == None:
            break
        rows.append(row)
    cursor.close()
    return rows
 

