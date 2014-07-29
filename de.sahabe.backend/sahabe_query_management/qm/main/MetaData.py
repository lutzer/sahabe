'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''

from db.main import DBApiModule as db


def addIconUrl(linkId, value, commit=True):
    conn = db.connect()
    db.insertToTable(conn, "meta_data", commit=commit,
                     link_id=linkId,
                     l_key="iconUrl",
                     value=value)
    return True
            
            
            
            