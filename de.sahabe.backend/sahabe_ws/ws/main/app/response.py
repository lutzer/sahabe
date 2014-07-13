'''
Created on Jul 13, 2014

@author: Maan Al Balkhi
'''

from flask import Response
from flask import json

headers = {"Access-Control-Allow-Origin":"http://0.0.0.0:8000",
           "Access-Control-Allow-Methods":"*",
           "Access-Control-Allow-Credentials":"true"}


def send400(message="operation failed", mimetype='application/json'):
    js = json.dumps({"message":message})
    resp = Response(js, status=400, mimetype=mimetype)
    
    for key, value in headers.iteritems():
        resp.headers.add(key, value)
    
    return resp
    
def send401(message="unauthorized", mimetype='application/json'):
    js = json.dumps({"message":message})
    resp = Response(js, status=401, mimetype=mimetype)
    
    for key, value in headers.iteritems():
        resp.headers.add(key, value)
    
    return resp

def send200(message="operation was successful", mimetype='application/json'):
    js = json.dumps({"message":message})
    resp = Response(js, status=200, mimetype=mimetype)

    for key, value in headers.iteritems():
        resp.headers.add(key, value)

    return resp
    
def sendData(data, status=200,  mimetype='application/json'):
    js = json.dumps(data)
    resp = Response(js, status=status, mimetype=mimetype)

    for key, value in headers.iteritems():
        resp.headers.add(key, value)

    return resp
