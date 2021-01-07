#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from utils import utils
from flask import Flask, request

app = Flask(__name__)
sat = utils.create_sat_from_env()
HOST = '0.0.0.0'
PORT = 5001
IN_ORBIT = bool(os.getenv("USE_ORBIT_PARAMETERS", "FALSE") == "TRUE")


def main():
    app.run(
        debug=True,
        port=PORT,
        host=HOST,

        # These settings are important because the virtual sat is not thread or
        # process safe.
        # The reloader creates multiple sats that can interfere with each other
        threaded=False,
        use_reloader=False
    )


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET' and not IN_ORBIT:
        tlm = sat.status()
        tlm["_links"] = {
            "telemetry history": "http://localhost:{}/history".format(PORT)
        }
        return tlm
    if request.method == 'POST' and not IN_ORBIT:
        try:
            res = sat.radio.deserialize(request.json)
            if res:
                return "Success!"
            else:
                return "There was a problem with that request", 400
        except SystemError as e:
            return str(e), 400
    return ({}, 204)


@app.route('/radio', methods=["POST"])
def radio():
    try:
        res = sat.radio.deserialize(request.json)
        if res:
            return "Success!"
        else:
            return "Bad request", 400
    except SystemError as e:
        return str(e), 400


@app.route('/debug', methods=["GET"])
def debug():
    return sat.status()


@app.route('/history', methods=["GET"])
def history():
    if request.method == 'GET' and not IN_ORBIT:
        history_array = sat.telemetry_subsystem.get_history()
        tlm = {
            "history": history_array,
            "_links": {
                "current": "http://localhost:{}/".format(PORT)
            }
        }
        return tlm
    return ({}, 204)


if __name__ == '__main__':
    main()
