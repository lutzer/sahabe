'''
Created on Jul 13, 2014

@author: Maan Al Balkhi
'''

import re
import ast
import string
import random
import datetime

from flask import json


def timeStamp():
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(timeStamp)
    
def randomText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def extractHomeUrl(url):
    if not url.endswith("/"):
        url += "/"
    
    if not url.startswith("http://"):
        url = "http://"+url
    
    if url.startswith("https://"):
        url = url.replace("https://", "http://")
        
    m = re.search("(http(:|s:)//(.+?)/)", url)
    return m.group(1)

def extractData(upload):
    data = ""
    dataFormat = upload.content_type 
    
    if dataFormat == "text/html":
        print "NOT IMPLEMENTED"
        #with open(upload.filename, "r") as html:
    
    elif dataFormat == "application/json":
        data = json.load(upload)
    
    elif dataFormat == "application/octet-stream":
        data = ast.literal_eval(upload.read())
    
    else:
        Exception(dataFormat+ " data formats is not supported ") 
    
    return data
    
    
    