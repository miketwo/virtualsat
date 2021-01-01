#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import utils
from flask import Flask, request

app = Flask(__name__)
sat = utils.create_sat_from_env()
HOST = '0.0.0.0'
PORT = 5001


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
    if request.method == 'GET':
        tlm = sat.status()
        tlm["_links"] = {
            "telemetry history": "http://localhost:{}/history".format(PORT)
        }
        return tlm
    if request.method == 'POST':
        try:
            res = sat.radio.deserialize(request.json)
            if res:
                return "Success!"
            else:
                return "Bad request", 400
        except SystemError as e:
            return str(e), 400


@app.route('/tlm', methods=["GET"])
def tlm():
    return sat.status()

@app.route('/history', methods=["GET"])
def history():
    if request.method == 'GET':
        history_array = sat.telemetry_subsystem.get_history()
        tlm = {
            "history": history_array,
            "_links": {
                "current": "http://localhost:{}/".format(PORT)
            }
        }
        return tlm


if __name__ == '__main__':
    main()
