'''
Created on Jun 12, 2014

@author: Maan Al Balkhi
'''
import DBApiModule
from DBApiModule import DataTypes as dt


def run(host="localhost", user="sahabe", pw="sahabe", db="sahabe"):
    
    """
    conn, table, primaryKey, uniqueList, notNulls, forgenKeys, *order, **kwargs
    """
    conn = DBApiModule.connect(host, user, pw, db)
    """
    user, link, search_table, tag, link_tag_map, link_group, link_group_map, meta_data, pw_hash 
    """
    DBApiModule.dropTable(conn, "pw_hash", "meta_data", "link_group_map", "link_group", "link_tag_map",
                          "tag", "search_table", "link", "user")
    
    """ user """
    DBApiModule.createTable(conn,
                            "user",
                            "id",
                            {"name", "email"},
                            {"id", "name", "email"},
                            {},
                            [],
                            "id", "name", "email",
                            id=dt.UUID, name=dt.VCHAR64, email=dt.VCHAR64)
    
    """ link """ 
    DBApiModule.createTable(conn,
                            "link",
                            "id",
                            {"user_id , url_hash"},
                            {"id", "user_id", "url", "url_hash","modified_at"},
                            {"user_id":"user.id"},
                            ["url","title","description", "type_name"],
                            "id", "user_id", "url", "url_hash","title", "description", "type_name", "modified_at",
                            id=dt.UUID, user_id=dt.UUID, url=dt.TEXT, url_hash=dt.MD5 ,title=dt.VCHAR255,
                            description=dt.TEXT, type_name=dt.VCHAR64 ,modified_at=dt.DATETIME)
    
    """ search_table """ 
    DBApiModule.createTable(conn,
                            "search_table",
                            "link_id",
                            {},
                            {"user_id", "link_id"},
                            {"user_id":"user.id", "link_id":"link.id"},
                            ["groups", "tags", "text"],
                            "user_id", "link_id", "groups", "tags", "text",
                            user_id=dt.UUID, link_id=dt.UUID,
                            groups=dt.VCHAR255, tags=dt.VCHAR255, text=dt.VCHAR255)
    
    """ tag """ 
    DBApiModule.createTable(conn,
                            "tag",
                            "id",
                            {"user_id, name"},
                            {"id", "user_id","name"},
                            {"user_id":"user.id"},
                            [],
                            "id", "user_id", "name",
                            id=dt.UUID, user_id=dt.UUID, name=dt.VCHAR64)
    
    """ link_tag_map """
    DBApiModule.createTable(conn,
                            "link_tag_map",
                            "tag_id, link_id",
                            {},
                            {"tag_id", "link_id"},
                            {"tag_id":"tag.id", "link_id":"link.id"},
                            [],
                            "tag_id", "link_id",
                            tag_id=dt.UUID, link_id=dt.UUID)
    
    """ link_group """ 
    DBApiModule.createTable(conn,
                            "link_group",
                            "id",
                            {"user_id, name"},
                            {"id", "user_id","name", "public"},
                            {"user_id":"user.id"},
                            [],
                            "id", "user_id", "name", "public",
                            id=dt.UUID, user_id=dt.UUID, name=dt.VCHAR64, public=dt.BOOL)
    
    """ link_group_map """
    DBApiModule.createTable(conn,
                            "link_group_map",
                            "group_id, link_id",
                            {},
                            {"group_id", "link_id"},
                            {"group_id":"link_group.id", "link_id":"link.id"},
                            [],
                            "group_id", "link_id",
                            group_id=dt.UUID, link_id=dt.UUID)
    
    """ meta_data """ 
    DBApiModule.createTable(conn,
                            "meta_data",
                            "link_id, l_key, value",
                            {},
                            {"link_id", "l_key", "value"},
                            {"link_id":"link.id"},
                            [],
                            "link_id", "l_key", "value",
                            link_id=dt.UUID, l_key=dt.VCHAR64, value=dt.VCHAR255)
    
    """ pw_hash """
    DBApiModule.createTable(conn,
                            "pw_hash",
                            "user_id",
                            {"user_id"},
                            {"user_id", "value", "salt"},
                            {"user_id":"user.id"},
                            [],
                            "user_id", "value", "salt",
                            user_id=dt.UUID, value=dt.SHA_2, salt=dt.CHAR64)
    conn.close()
    
""" don't run if its an external call """
if __name__=='__main__':
    run()
    
  
