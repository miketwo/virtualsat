# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import core
import kbhit
from datetime import datetime
import random

def main():
    kb = kbhit.KBHit()
    sat = core.create_random_sat()
    print('Hit any key, or ESC to exit')

    while True:
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27: # ESC
                break
            if c == 'r':
                sat.COMMANDS['recharge']()
            if c == 'n':
                sat.COMMANDS['normal']()
            if c == 'p':
                sat.add_command_scheduled_pics(datetime.now(), 30)
            if c == 'd':
                pics = [p for p in sat.pictures if p is not None]
                if len(pics) > 0:
                    sat.downlink_file(random.choice(pics))
                else:
                    print("No pics to download")
            if c == 'l':
                sat.list_pics()

            print(c)

    kb.set_normal_term()


if __name__ == '__main__':
    main()
