# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from satellite import core, kbhit
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
sat = core.create_random_sat()

def main():
    app.run(debug=True, port=5001, host='0.0.0.0', threaded=False, use_reloader=False)  #blocking

@app.route('/')
def index():
    if request.method == 'GET':
        return sat.status()

@app.route('/radio', methods=["POST"])
def radio():
    if request.method == 'POST':
        res = sat.radio.deserialize(request.json)
        if res:
            return "Success!"
        else:
            return "Bad request", 400

#deprecated
# def cli_interface():
#     kb = kbhit.KBHit()
#     sat = core.create_random_sat()
#     print('Hit any key, or ESC to exit')

#     while True:
#         if kb.kbhit():
#             c = kb.getch()
#             if ord(c) == 27: # ESC
#                 break
#             if c == 'r':
#                 sat.command_subsystem._COMMANDS['recharge']()
#             if c == 'n':
#                 sat.command_subsystem._COMMANDS['normal']()
#             if c == 'p':
#                 sat.add_command_scheduled_pics(datetime.now(), 30)
#             if c == 'd':
#                 sat.imaging_subsystem.pop()
#             if c == 'l':
#                 sat.list_pics()

#             print(c)

#     kb.set_normal_term()


if __name__ == '__main__':
    main()
