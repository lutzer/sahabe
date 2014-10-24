'''
Created on Jul 12, 2014

@author: Maan Al Balkhi
'''


def convertLinksSetToDicts(resultSet):
    '''
    @param resultSet: results set of a presentable link
    @return: list of dictionaries -keys = id, user, url, title, typename, modifiedAt, logoUrl
    '''
    dicts = []
    for link in resultSet:
            dicts.append({"linkId":link[0],
                          "url":link[1],
                          "title":link[2],
                          "description":link[3],
                          "typeName":link[4],
                          "modifiedAt":link[5],
                          "iconUrl":link[6]})
    return dicts
    