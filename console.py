#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cmd import Cmd
import requests
import time

sat_url = "http://sat:5001/"


class MyPrompt(Cmd):
    prompt = 'Satellite> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print('Exit the application. Shorthand: x q Ctrl-D.')

    def do_power(self, arg):
        cmd = {"subsystem": "power"}
        if arg == 'r':
            print("Asking for recharge mode...")
            cmd.update({ "mode": "recharge"})
            res = requests.post(sat_url, json=cmd)
            print(res)
        elif arg == 'n':
            print("Asking for normal mode...")
            cmd.update({ "mode": "normal"})
            res = requests.post(sat_url, json=cmd)
            print(res)
        else:
            self.help_power()

    def help_power(self):
        print('''Adjust power mode.
            power r -- recharge
            power n -- normal''')

    def do_value(self, arg):
        cmd = {"subsystem": "value"}

        actions = {
            "c": {**cmd, "value": "create"},
            "d": {**cmd,  "value": "download"},
        }
        if arg not in actions:
            return self.help_value()
        cmd = actions[arg]
        res = requests.post(sat_url, json=cmd)
        print(res.text)

    def help_value(self):
        print('''value subsystem:
            value c - create value
            value d - download value''')

    def do_sched(self, arg):
        cmd = {
            "subsystem": "sched",
            "time": str(time.time() + 10),
            "command": {
                "subsystem": "power",
                "mode": "recharge"
            }
        }
        # if arg not in actions:
            # return self.help_value()
        res = requests.post(sat_url, json=cmd)
        print(res.text)

    def do_ping(self, inp):
        print("Tbd.... ping sat")

    def help_ping(self):
        print('''Simple Ping
            ping - ping the satellite''')

    def emptyline(self):
        print(requests.get(sat_url + "/tlm").json())

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("No command found for '{}'".format(inp))


if __name__ == '__main__':
    MyPrompt().cmdloop()  # blocking
