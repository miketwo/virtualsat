# -*- coding: utf-8 -*-
import sched
import random
import time
from datetime import datetime, timedelta
from functools import partialmethod

from pyorbital import tlefile
from pyorbital.orbital import Orbital
from apscheduler.schedulers.background import BackgroundScheduler


def parse_tles(raw_data):
        """Parse all the TLEs in the given raw text data."""
        tles = []
        line1, line2 = None, None
        raw_data = raw_data.split('\n')
        for row in raw_data:
            if row.startswith('1 '):
                line1 = row
            elif row.startswith('2 '):
                line2 = row
            else:
                name = row
            if line1 is not None and line2 is not None:
                try:
                    tle = tlefile.Tle(name, line1=line1, line2=line2)
                except ValueError:
                    logging.warning(
                        "Invalid data found - line1: %s, line2: %s",
                        line1, line2)
                else:
                    tles.append(tle)
                line1, line2 = None, None
        return tles

# Hack to get Starlink sats loaded. Requires a file downloaded from
# celestrak
def read_satfile():
    filepath = "/app/starlink.txt"
    with open(filepath, 'r') as content_file:
        content = content_file.read()
    return content

def create_random_sat():
    raw_data = read_satfile()
    tles = parse_tles(raw_data)
    sats = tles
    acceptable_sats = sats #[s for s in sats if "noaa" in s.lower()]
    print("Number of acceptable_sats: {}".format(len(acceptable_sats)))
    selected_sat = random.choice(acceptable_sats)
    # tle1 = "1 47167U 20088AX  20364.91667824  .00060804  00000-0  66636-3 0  9999"
    # tle2 = "2 47167  53.0531 181.7584 0001052  62.9760  12.0163 15.62698232  1778"
    return Satellite(selected_sat.platform, selected_sat.line1, selected_sat.line2)


class Satellite(object):
    TLM_MAX = 20
    TLM_RECORD_INTERVAL = 5
    PICS_MAX = 5

    def __init__(self, name, tle1, tle2):
        super(Satellite, self).__init__()
        self.name = name
        print("Creating Satellite named {}".format(name))
        print("Please wait...")
        self.orb = Orbital(name, line1=tle1, line2=tle2)
        
        self.reboot_counter = 0
        self.command_id = 1

        self.power = 100
        self.power_mode = "normal"

        self.tlm_history = [None for x in range(self.TLM_MAX)]
        self.tlm_idx = 0

        self.pictures = [None for x in range(self.PICS_MAX)]
        self.pic_idx = 0
        
        self.setup_schedulers()

        print(self)

        self.COMMANDS = {
            "recharge": self.set_recharge,
            "normal": self.set_normal,
        }

    def set_power_mode(self, mode):
        print("POWER MODE --> {}".format(mode))
        self.power_mode = mode

    set_recharge = partialmethod(set_power_mode, "recharge")
    set_normal = partialmethod(set_power_mode, "normal")

    def setup_schedulers(self):
        self.command_scheduler = BackgroundScheduler()
        self.internal_scheduler = BackgroundScheduler()

        self.internal_scheduler.add_job(self.update_power, 'interval', seconds=1)
        self.internal_scheduler.add_job(self.record_tlm, 'interval', seconds=self.TLM_RECORD_INTERVAL)

        self.command_scheduler.start()
        self.internal_scheduler.start()
       
        
    def __str__(self):
        return "\n{}\n{}\n{}\nCOMMANDS:\n{}".format(self.name, self.orb.tle.line1, self.orb.tle.line2, self.command_scheduler.get_jobs())

    def add_command(self, command, target_datetime):
        tmp = str(self.command_id)
        name = "CMD #{}: {}".format(tmp, command)
        self.command_scheduler.add_job(self.COMMANDS[command], 'date', run_date=target_datetime, id=tmp, name=name)
        print("Added command {}".format(tmp))
        self.command_id += 1
        return tmp

    def remove_command(self, command_id):
        self.command_scheduler.remove_job(command_id)

    def clear_commands(self):
        cmds = [j.id for j in self.command_scheduler.get_jobs()]
        for cmd in cmds:
            self.command_scheduler.remove_job(cmd)

    def print_commands(self):
        print("COMMANDS:")
        cmds = [j.name for j in self.command_scheduler.get_jobs()]
        for cmd in cmds:
            print("  {}".format(cmd))

    def add_command_scheduled_pics(self, start_date, duration_sec):
        tmp = str(self.command_id)
        name = "CMD #{}: Picture Window @ {} for {} seconds".format(tmp, start_date, duration_sec)
        self.command_scheduler.add_job(
            self.take_pic, 
            'interval', 
            seconds=5, 
            start_date=start_date, 
            end_date=start_date+timedelta(seconds=duration_sec),
            id=tmp,
            name=name)
        print("Added command {}".format(tmp))
        self.command_id += 1
        return tmp

    def update_power(self):
        print("{} -- {}".format(self.power_mode, self.power))
        if self.power_mode is "recharge" and self.power < 100:
            self.power += 1
        elif self.power_mode is "normal" and self.power > 0:
            self.power -=1
        else:
            None
        

    def current_position(self):
        return self.orb.get_lonlatalt(datetime.now())

    def is_visible_from(self, lat,lon):
        az, el = self.get_look(lat, lon)
        return el > 0

    def get_look(self, lat,lon):
        return self.orb.get_observer_look(datetime.now(),lat,lon,0)

    def record_tlm(self):
        self.tlm_history[self.tlm_idx%self.TLM_MAX] = self.power
        self.tlm_idx += 1
        print("Telemetry: {}".format([x for x in self.tlm_history if x is not None]))

    def take_pic(self):
        if self.power_mode is not "normal":
            print("ERROR: Must be in normal power mode to take pictures")
            return
        if self.power <= 5:
            print("ERROR: Not enough power to take picture")
            return
        print("Taking a picture")
        self.pictures[self.pic_idx%self.PICS_MAX] = "Pic{}".format(self.pic_idx)
        self.pic_idx += 1
        self.power -= 5
        print(self.pictures)

    def downlink_file(self, pic_name):
        if self.power >= 10:
            try:
                idx = self.pictures.index(pic_name)
                self.pictures[idx] = None
                self.power -= 10
                print("Downloaded {}".format(pic_name))
            except Exception as e:
                print(e)
        else:
            print("Not enough power to tx pic")


    def list_pics(self):
        if self.power >= 10:
            print(self.pictures)
            self.power -= 10
            return self.pictures
        else:
            print("Not enough power to tx list")
        return None    


def add_two_things(a, b):
    return a+b

