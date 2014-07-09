'''
Created on Jul 5, 2014

@author: Maan Al Balkhi
'''
import impl.DBApiModule as db
import urllib
import string
import re
import os.path as path

def foo1(s):
    print 'from ' + foo1.__name__ 
    return 'baller'
    
@foo1
def foo2(bla):
    print bla
    print 'no arguments for ' + foo2.__name__

conn = db.connect()
rows = db.selectFrom(conn, {"link"}, "id","url")
for row in rows:
    linkId = row[0]
    url = row[1]
    
    m = re.search("(http(:|s:)//(.+?)/)", url)
    iconUrl = m.group(1)+"favicon.ico"
    site = m.group(3)
    iconLink = "static/" + site +"_logo.ico"
    print iconUrl
    #print iconLink
    print
    
    #db.insertToTable(conn, "meta_data", link_id=linkId, l_key="logo", value=iconLink)
     
    '''
    if not path.isfile(iconLink):
        print "retrieve icon"
        urllib.urlretrieve(iconUrl, iconLink)
    '''