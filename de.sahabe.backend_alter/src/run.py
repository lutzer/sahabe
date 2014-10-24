'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
@attention: this script runs a development web server with the application.
'''

import config

from app import app

'''
Start a web server with port 5000 on local host.
For specific address and port add the parameters host = xxx and port = xxx    
'''
if __name__ == "__main__": 
    app.run(debug = config.debug , host="0.0.0.0")





