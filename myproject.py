from flask import Flask,request, abort
import requests
import os
import sys
import subprocess
from StringIO import StringIO 
from tempfile import NamedTemporaryFile
from werkzeug.contrib.cache import SimpleCache 

cache = SimpleCache()
application = Flask(__name__)

@application.route('/')
def index():
    return "Give you the number of colors in a picture, visit:<a>/api/num_colors?src=SOMEURL</a>"
@application.route('/api/num_colors')
def colorcount():
    
    url = request.args.get('src')
    imgurl = str(url)
    visited = cache.get(imgurl)
    if not visited:
        
        getfile = requests.get(url, timeout=5)
    
        if 'image' not in getfile.headers['content-type']:
            abort(400, "Not valid image")
     
        with  NamedTemporaryFile() as temp_file:
	    temp_file.write(getfile.content)
	    temp_file.seek(0,0)
	    tmpimage = temp_file.name
        
            numcol =  subprocess.check_output(["/usr/bin/identify","-format","%k",tmpimage])
            cache.set(imgurl,numcol, timeout=86400)

            return numcol
    else:
        return visited
if __name__ == "__main__":
    application.run(host='0.0.0.0')
