'''
Created on Oct 24, 2014

@author: Maan Al Balkhi
'''

def converGroupsSetToDict(resultsSet):
    dicts = []
    for group in resultsSet:
        dicts.append({"id":group[0],
                     "name":group[1],
                     "public":group[2]})
    return dicts
