# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import groundstation
from flask import Flask, request
import time
import json

app = Flask(__name__)
gs = groundstation.core.Groundstation("STL GroundStation1", 38.6270, -90.1994)

def main():
    app.run(debug=True, host='0.0.0.0', threaded=False, use_reloader=False)  #blocking

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return gs.status()
    if request.method == 'POST':
        gs.send_command(request.form)
        return "Successful post"

@app.route('/target', methods=["GET", "POST"])
def target():
    if request.method == 'GET':
        return json.dumps(gs.target)
    if request.method == 'POST':
        app.logger.debug(request)
        filtered = {k:v for (k,v) in dict(request.form).items() if k in ["name", "line1", "line2"]}
        app.logger.debug(filtered)
        gs.set_target(**filtered)
        return "Successful post"

if __name__ == '__main__':
    main()
