#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cmd import Cmd
import requests
from datetime import datetime,timedelta

SAT_URL = "http://sat:5001/"
GS_URL = "http://gs:5000/"

COMMANDS = {
    "satellite": {
        "power": {
            "r": {
                "subsystem": "power",
                "mode": "recharge"
            },
            "n": {
                "subsystem": "power",
                "mode": "normal"
            },
        },
        "value": {
            "c": {
                "subsystem": "value", 
                "value": "create"
            },
            "d": {
                "subsystem": "value",  
                "value": "download"
            },            
        },
        "sched": {
            "subsystem": "sched",
        }
    },
    "groundstation": {
        "track": {}
    }
}


class MainMenu(Cmd):
    prompt = 'Console> '
    intro = "Welcome! Type ? to list commands. Please choose satellite or groundstation:"

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

    # Short aliases
    do_sat = do_satellite
    help_sat = help_satellite
    do_gs = do_groundstation
    help_gs = help_groundstation

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
        cmd = COMMANDS["satellite"]["power"].get(arg)
        if not cmd:
            self.help_power()
        else:
            res = requests.post(SAT_URL, json=cmd)
            print(res.status_code)

    def help_power(self):
        print('''Adjust power mode.
            power r -- recharge
            power n -- normal''')

    def do_value(self, arg):
        cmd = COMMANDS["satellite"]["value"].get(arg)
        if not cmd:
            self.help_value()
        else:
            res = requests.post(SAT_URL, json=cmd)
            print(res.status_code)

    def help_value(self):
        print('''value subsystem:
            value c - create value
            value d - download value''')

    def do_sched(self, arg):
        # sched TIME SUBSYSTEM CMD
        self._sched_helper(arg, relative=False)

    def help_sched(self):
        print("""Scheduling a command:
            sched <UTC TIME> <SUBSYSTEM> <CMD>

            Example:
            sched 1609459200 power r  -- sets power to recharge at midnight on New Year's 2021
            """)

    def do_rsched(self, arg):
        # rsched DELTA_TIME_SECONDS SUBSYSTEM CMD
        self._sched_helper(arg, relative=True)

    def _sched_helper(self, arg, relative):
        try:
            time, subsystem, cmd = arg.split()
            if relative:
                dt = datetime.utcnow() + timedelta(seconds=int(time))
            else:
                dt = datetime.utcfromtimestamp(int(time))
            subcommand = COMMANDS['satellite'][subsystem][cmd]
            send_cmd = {
                "subsystem": "sched",
                "time": str(dt.timestamp()),
                "command": subcommand
            }
        except KeyError as e:
            print("Command '{} {}' not found.".format(subsystem, cmd))
            return
        except Exception as e:
            print(e)
            return
        res = requests.post(SAT_URL, json=send_cmd)        

    def help_rsched(self):
        print("""Scheduling a command:
            sched <DELTA_TIME_SECONDS> <SUBSYSTEM> <CMD>

            Example:
            sched 10 power r  -- sets power to recharge in 10 seconds
            """)

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
