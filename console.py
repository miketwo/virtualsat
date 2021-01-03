#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cmd import Cmd
import requests
from datetime import datetime

SAT_URL = "http://sat:5001/"
GS_URL = "http://gs:5000/"

class MainMenu(Cmd):
    prompt = 'Console> '
    intro = "Welcome! Are you talking to a satellite or groundstation?"

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_satellite(self, s):
        i = SatelliteConsole()
        i.cmdloop()

    def help_satellite(self):
        print("Talk to the satellite. It must not be in orbit.")

    def do_groundstation(self, s):
        i = GroundstationConsole()
        i.cmdloop()

    def help_groundstation(self, s):
        print("Talk to the groundstation.")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("No command found for '{}'".format(inp))


class GroundstationConsole(Cmd):
    prompt = 'Console:Groundstation> '
    intro = "Welcome! Type ? to list commands"

    def validate(self, tle1, tle2):
        return True

    def do_exit(self, inp):
        return True

    def do_track(self, s):
        name = input("Satellite Name> ")
        tle1 = input("TLE Line 1> ")
        tle2 = input("TLE Line 2> ")
        if not self.validate(tle1, tle2):
            print("Something appears to be wrong with the TLEs")
        date = {
            "name": name,
            "line1": tle1,
            "line2": tle2,
        }
        res = requests.post(GS_URL + "target", json=date)
        print(res)


    def emptyline(self):
        res = requests.get(GS_URL)
        if res.status_code == 204:
            pass
        elif res:
            print(res.json())
        else:
            pass

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("No command found for '{}'".format(inp))


class SatelliteConsole(Cmd):
    prompt = 'Console:Satellite> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        return True

    def help_exit(self):
        print('Return to main menu. Shorthand: x q')

    def do_power(self, arg):
        cmd = {"subsystem": "power"}
        if arg == 'r':
            cmd.update({ "mode": "recharge"})
            res = requests.post(SAT_URL, json=cmd)
        elif arg == 'n':
            cmd.update({ "mode": "normal"})
            res = requests.post(SAT_URL, json=cmd)
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
        requests.post(SAT_URL, json=cmd)

    def help_value(self):
        print('''value subsystem:
            value c - create value
            value d - download value''')

    def do_sched(self, arg):
        cmd = {
            "subsystem": "sched",
            "time": str(datetime.utcnow().timestamp() + 10),
            "command": {
                "subsystem": "power",
                "mode": "recharge"
            }
        }
        # if arg not in actions:
            # return self.help_value()
        res = requests.post(SAT_URL, json=cmd)

    def do_ping(self, inp):
        print("Tbd.... ping sat")

    def help_ping(self):
        print('''Simple Ping
            ping - ping the satellite''')

    def emptyline(self):
        res = requests.get(SAT_URL)
        if res.status_code == 204:
            pass
        elif res:
            print(res.json())
        else:
            pass

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("No command found for '{}'".format(inp))


if __name__ == '__main__':
    MainMenu().cmdloop()  # blocking
