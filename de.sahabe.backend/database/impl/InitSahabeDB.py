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
                            "id", "name", "email",
                            id=dt.UUID, name=dt.VCHAR64, email=dt.VCHAR64)
    
    """ link """ 
    DBApiModule.createTable(conn,
                            "link",
                            "id",
                            {},
                            {"id", "user_id", "url", "modified_at"},
                            {"user_id":"user.id"},
                            "id", "user_id", "url", "title", "description", "type_name", "modified_at",
                            id=dt.UUID, user_id=dt.UUID, url=dt.VCHAR256, title=dt.CHAR64,
                            description=dt.VCHAR256, type_name=dt.VCHAR64 ,modified_at=dt.DATETIME)
    
    """ search_table """ 
    DBApiModule.createTable(conn,
                            "search_table",
                            "user_id, link_id",
                            {},
                            {"user_id", "link_id"},
                            {"user_id":"user.id", "link_id":"link.id"},
                            "user_id", "link_id", "groups", "tags", "text",
                            user_id=dt.UUID, link_id=dt.UUID,
                            groups=dt.VCHAR256, tags=dt.VCHAR256, text=dt.VCHAR256)
    
    """ tag """ 
    DBApiModule.createTable(conn,
                            "tag",
                            "id",
                            {},
                            {"id", "name"},
                            {},
                            "id", "name",
                            id=dt.UUID, name=dt.VCHAR64)
    
    """ link_tag_map """
    DBApiModule.createTable(conn,
                            "link_tag_map",
                            "tag_id, link_id",
                            {},
                            {"tag_id", "link_id"},
                            {"tag_id":"tag.id", "link_id":"link.id"},
                            "tag_id", "link_id",
                            tag_id=dt.UUID, link_id=dt.UUID)
    
    """ link_group """ 
    DBApiModule.createTable(conn,
                            "link_group",
                            "id",
                            {},
                            {"id", "name", "public"},
                            {},
                            "id", "name", "public",
                            id=dt.UUID, name=dt.VCHAR256, public=dt.BOOL)
    
    """ link_group_map """
    DBApiModule.createTable(conn,
                            "link_group_map",
                            "group_id, link_id",
                            {},
                            {"group_id", "link_id"},
                            {"group_id":"link_group.id", "link_id":"link.id"},
                            "group_id", "link_id",
                            group_id=dt.UUID, link_id=dt.UUID)
    
    """ meta_data """ 
    DBApiModule.createTable(conn,
                            "meta_data",
                            "id",
                            {},
                            {"link_id", "v_key", "value"},
                            {"link_id":"link.id"},
                            "id", "link_id", "v_key", "value",
                            id=dt.UUID, link_id=dt.UUID,
                            v_key=dt.VCHAR64, value=dt.VCHAR64)
    
    """ pw_hash """
    DBApiModule.createTable(conn,
                            "pw_hash",
                            "user_id",
                            {"user_id", "value"},
                            {"user_id", "value", "salt"},
                            {"user_id":"user.id"},
                            "user_id", "value", "salt",
                            user_id=dt.UUID, value=dt.SHA_2, salt=dt.CHAR64)
    conn.close()
    
""" don't run if its an external call """
if __name__=='__main__':
    run()
    
  
