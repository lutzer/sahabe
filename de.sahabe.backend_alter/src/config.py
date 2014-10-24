'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''

import os


basedir = os.path.abspath(os.path.dirname(__file__))

tmp = "../../../tmp"
log = tmp + "/sahabe.log"
debug = True
 
#activates the cross-site request forgery (make the more secure).
#See: http://en.wikipedia.org/wiki/Cross-site_request_forgery
CSRF_ENABLED = True
#is only needed when CSRF is enabled, and is used to create a cryptographic token 
#that is used to validate a form. make sure to set the secret key to something
#that is difficult to guess.
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#openID providers To make it easier for users to login
OPENID_PROVIDERS = [
    { 'name': 'Facebook', 'url': 'http://facebook-openid.appspot.com/'},
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]