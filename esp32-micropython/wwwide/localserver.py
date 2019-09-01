# this is to run text editor locally, for development of editor itself

from flask import Flask, request, Response
import os
import re

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app._static_folder = ''

@app.route("/file_list")
def file_list():
    path = request.args.get('path', '')
    if re.match(r'^/?$', path):
        return "boot.py;config/;lib/;assets/;pinouts/;util/;examples/;webrepl_cfg.py;wwwide/"
    if re.match(r'^/?config/?$', path):
        return "test1.py;subdir/;subdir3/;test2.py"
    if re.match(r'^/?config/subdir/?$', path):
        return "hello.py"
    return ""

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<filename>.gz')
def gzipped_static(filename):
    with open(filename + '.gz', 'rb') as f:
        r = Response(f.read())
        r.headers['Content-Encoding'] = 'gzip'
        r.headers['Content-Type'] = 'application/javascript'
    return r


if __name__ == "__main__":
    app.run(debug=True)
