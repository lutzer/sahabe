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
                          "typeName":link[3],
                          "modifiedAt":link[4],
                          "logo":link[5]})
    return dicts
    