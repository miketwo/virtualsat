#!/usr/bin/env python
# -*- coding: utf-8 -*-
import groundstation
from utils import utils
from flask import Flask, request
import json

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000

gs = utils.create_gs_from_env()


def main():
    app.run(
        debug=True,
        port=PORT,
        host=HOST,

        # These settings are important because the virtual gs is not thread or
        # process safe.
        # The reloader creates multiple instances that can interfere with each other
        threaded=False,
        use_reloader=False)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return gs.status()
    if request.method == 'POST':
        try:
            res = gs.send_command(request.json)
            if res:
                return "Success!"
            else:
                return "Bad request", 400
        except SystemError as e:
            return str(e), 400
        except Exception as e:
            print("Generic error")
            return str(e), 500


@app.route('/target', methods=["GET", "POST"])
def target():
    if request.method == 'GET':
        return json.dumps(gs.target)
    if request.method == 'POST':
        app.logger.debug(request)
        filtered = {k:v for (k,v) in dict(request.json).items() if k in ["name", "line1", "line2"]}
        app.logger.debug(filtered)
        gs.tracking_system.set_target(**filtered)
        return "Successful post"


if __name__ == '__main__':
    main()
