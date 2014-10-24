'''
Created on Oct 21, 2014

@author: Maan Al Balkhi
'''

def converUserToDict(user):
    userDict = {"id":user.id,
                "username":user.username,
                "email":user.email}
    return userDict