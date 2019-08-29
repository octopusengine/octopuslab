import os
import time
from machine import Pin

import wifi

import uftpd

from microWebSrv import MicroWebSrv

@MicroWebSrv.route('/file_list')
def _httpHandlerTestGet(httpClient, httpResponse) :
    content = ""
    l=os.listdir()
    for f in l:
        s=os.stat(f)
        content = content + f + ";"
    httpResponse.WriteResponseOk( headers = None, contentType = "text/html", contentCharset = "UTF-8", content = content )

mws = MicroWebSrv(webPath='www/')      # TCP port 80 and files in /flash/www
mws.Start(threaded=True) # Starts server in a new thread