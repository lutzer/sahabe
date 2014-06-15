'''
Created on Jun 12, 2014

@author: maan al balkhi
'''
import DBApiModule
from DBApiModule import DataTypes as dt


def run(host="localhost", user="sahabe", pw="sahabe", db="sahabe"):
    
    """
    conn, table, primaryKey, uniqueList, notNulls, forgenKeys, *order, **kwargs
    """
    conn = DBApiModule.connect(host, user, pw, db)
    """
    user, category, tag, link, tag_map, pw_hash 
    """
    DBApiModule.dropTable(conn, "pw_hash", "tag_map", "link", "tag", "category", "user")
    
    """ user """
    DBApiModule.createTable(conn,
                            "user",
                            "id",
                            {"id", "name", "email"},
                            {"id", "name", "email"},
                            {},
                            "id", "name", "email",
                            id=dt.UUID, name=dt.VCHAR64, email=dt.VCHAR64)
    
    """ category """
    DBApiModule.createTable(conn,
                            "category",
                            "id",
                            {"id", "user_id"},
                            {"id", "user_id", "name"},
                            {"user_id":"user.id"},
                            "id", "user_id", "name",
                            id=dt.UUID, user_id=dt.UUID, name=dt.VCHAR64)
    
    """ link """ 
    DBApiModule.createTable(conn,
                            "link",
                            "id",
                            {"id", "user_id", "category_id"},
                            {"id", "user_id", "category_id", "url", "create_date"},
                            {"user_id":"user.id", "category_id":"category.id"},
                            "id", "user_id", "category_id", "url", "name", "description", "create_date",
                            id=dt.UUID, user_id=dt.UUID, category_id=dt.UUID, url=dt.VCHAR255,
                            name=dt.CHAR64, description=dt.VCHAR255, create_date=dt.DATETIME)
    
    """ tag """ 
    DBApiModule.createTable(conn,
                            "tag",
                            "id",
                            {"id", "user_id"},
                            {"id", "user_id", "name"},
                            {"user_id":"user.id"},
                            "id", "user_id", "name", "group_tag",
                            id=dt.UUID, user_id=dt.UUID, name=dt.VCHAR64, group_tag=dt.BOOL)
    
    """ tag_map """
    DBApiModule.createTable(conn,
                            "tag_map",
                            None,
                            {"link_id", "tag_id"},
                            {"link_id", "tag_id"},
                            {"link_id":"link.id", "tag_id":"tag.id"},
                            "link_id", "tag_id",
                            link_id=dt.UUID, tag_id=dt.UUID)
    
    """ pw_hash """
    DBApiModule.createTable(conn,
                            "pw_hash",
                            None,
                            {"user_id", "value", "salt"},
                            {"user_id", "value", "salt"},
                            {"user_id":"user.id"},
                            "user_id", "value", "salt",
                            user_id=dt.UUID, value=dt.SHA_2, salt=dt.CHAR64)
    conn.close()
    
""" don't run if its an external call """
if __name__=='__main__':
    run()
    
  
