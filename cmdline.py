#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cmd import Cmd
import requests

url = "http://sat:5001/radio"

class MyPrompt(Cmd):
    prompt = 'Satellite/GS> '
    intro = "Welcome! Type ? to list commands"
 
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('Exit the application. Shorthand: x q Ctrl-D.')
 
    def do_power(self, arg):
        cmd = {"subsystem": "power"}
        if arg == 'r':
            print("recharge mode")
            cmd.update({ "mode": "recharge"})
            res = requests.post(url, json=cmd)
            print(res)
        elif arg == 'n':
            print("normal mode")
            cmd.update({ "mode": "normal"})
            res = requests.post(url, json=cmd)
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
        print(cmd)
        res = requests.post(url, json=cmd)
        print(res.text)

    def help_image(self):
        print('''Image subsystem:
            image t - take image
            image d - download image
            image c - clear images''')

    def do_tlm(self, arg):
        print("tbd")
 
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))
 
    do_EOF = do_exit
    help_EOF = help_exit
 
if __name__ == '__main__':
    MyPrompt().cmdloop()  # blocking
