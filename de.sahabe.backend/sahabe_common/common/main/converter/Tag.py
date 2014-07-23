'''
Created on Jul 23, 2014

@author: Maan Al Balkhi
'''

def converTagsSetToDict(resultsSet):
    dicts = []
    for tag in resultsSet:
        dicts.append({"id":tag[0],
                     "name":tag[1]})
    return dicts