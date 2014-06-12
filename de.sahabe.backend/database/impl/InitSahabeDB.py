'''
Created on Jun 12, 2014

@author: maan al balkhi
'''
import DBApiModule
from DBApiModule import DataTypes as dt

"""
conn, table, primaryKey, uniqueList, notNulls, forgenKeys, *order, **kwargs
"""
conn = DBApiModule.connect("localhost", "sahabe", "sahabe", "sahabe")
"""
user, cat, tag, link, tag_map, pw_hash 
"""

""" user """
DBApiModule.createTable(conn,
                        "user",
                        "id",
                        {"id", "email"},
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

""" tag """ 
DBApiModule.createTable(conn,
                        "tag",
                        "id",
                        {"id", "user_id"},
                        {"id", "user_id", "name"},
                        {"user_id":"user.id"},
                        "id", "user_id", "name", "group_tag",
                        id=dt.UUID, user_id=dt.UUID, name=dt.VCHAR64, group_tag=dt.BOOL)

""" link """ 
DBApiModule.createTable(conn,
                        "link",
                        "id",
                        {"id", "user_id", "category_id"},
                        {"id", "user_id", "category_id", "url", "name", "create_date"},
                        {"user_id":"user.id", "category_id":"category.id"},
                        "id", "user_id", "category_id", "url", "name", "description", "create_date",
                        id=dt.UUID, user_id=dt.UUID, category_id=dt.UUID, url=dt.VCHAR255,
                        name=dt.CHAR64, description=dt.VCHAR255, create_date=dt.DATE)

""" tag_map """
DBApiModule.createTable(conn,
                        "tag_map",
                        "id",
                        {"id", "link_id", "tag_id"},
                        {"id", "link_id", "tag_id"},
                        {"link_id":"link.id", "tag_id":"tag.id"},
                        "id", "link_id", "tag_id",
                        id=dt.UUID, link_id=dt.UUID, tag_id=dt.UUID)

""" pw_hash """
DBApiModule.createTable(conn,
                        "pw_hash",
                        None,
                        {"user_id", "value", "salt"},
                        {"user_id", "value", "salt"},
                        {"user_id":"user.id"},
                        "user_id", "value", "salt",
                        user_id=dt.UUID, value=dt.SHA_2, salt=dt.CHAR64)




