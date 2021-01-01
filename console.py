#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cmd import Cmd
import requests

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

    def do_image(self, arg):
        cmd = {"subsystem": "image"}

        actions = {
            "t": {**cmd , "image": "take"},
            "d": {**cmd,  "image": "download"},
            "c": {**cmd,  "image": "clear"}
        }
        if arg not in actions:
            return self.help_image()
        cmd = actions[arg]
        res = requests.post(sat_url, json=cmd)
        print(res.text)

    def help_image(self):
        print('''Image subsystem:
            image t - take image
            image d - download image
            image c - clear images''')

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
