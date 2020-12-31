# -*- coding: utf-8 -*-
import sched
import random
import time
import json
from datetime import datetime, timedelta
from functools import partial, partialmethod

from pyorbital import tlefile
from pyorbital.orbital import Orbital
from apscheduler.schedulers.background import BackgroundScheduler

from satellite.power import PowerSubsystem
from satellite.telemetry import TelemetrySubsystem
from satellite.images import ImagingSubsystem
from satellite.dispatch import DispatchSubsystem
from satellite.schedule import SchedulerSubsystem
from satellite.comms import CommunicationSubsystem

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
    #selected_sat = random.choice(acceptable_sats)
    selected_sat = acceptable_sats[0]
    # tle1 = "1 47167U 20088AX  20364.91667824  .00060804  00000-0  66636-3 0  9999"
    # tle2 = "2 47167  53.0531 181.7584 0001052  62.9760  12.0163 15.62698232  1778"
    return Satellite(selected_sat.platform, selected_sat.line1, selected_sat.line2)


class Satellite(object):

    def __init__(self, name, tle1, tle2):
        super().__init__()
        self.name = name

        print("Creating Satellite named {}".format(name))
        print("Please wait...")

        self.orb = Orbital(name, line1=tle1, line2=tle2)
        self.power_subsystem = PowerSubsystem()
        self.imaging_subsystem = ImagingSubsystem(self.power_subsystem)

        self._dispatcher = DispatchSubsystem()
        self._dispatcher.register_subsystem("power", self.power_subsystem)
        self._dispatcher.register_subsystem("image", self.imaging_subsystem)

        self.radio = CommunicationSubsystem(self._dispatcher)

        self._scheduler = SchedulerSubsystem(self._dispatcher)

        self.telemetry_subsystem = TelemetrySubsystem()
        self.telemetry_subsystem.register(self.power_subsystem.get_tlm)
        self.telemetry_subsystem.register(self.imaging_subsystem.get_tlm)
        self.telemetry_subsystem.register(self._scheduler.get_tlm)
        self.telemetry_subsystem.register(self._dispatcher.get_tlm)
        
        print(self)

    def __str__(self):
        return "\n{}\n{}\n{}".format(self.name, self.orb.tle.line1, self.orb.tle.line2)

    def status(self):
        return dict(self.telemetry_subsystem.get_tlm())

    def schedule_command(self, *args, **kwargs):
        self._scheduler.schedule_command(*args, **kwargs)

    def schedule_command_scheduled_pics(self, *args, **kwargs):
        self._scheduler.schedule_command_scheduled_pics(*args, **kwargs)

    def print_commands(self, *args, **kwargs):
        self._scheduler.print_commands(*args, **kwargs)

    def current_position(self):
        return self.orb.get_lonlatalt(datetime.now())

    def is_visible_from(self, lat,lon):
        az, el = self.get_look(lat, lon)
        return el > 0

    def get_look(self, lat,lon):
        return self.orb.get_observer_look(datetime.now(),lat,lon,0)

    def take_pic(self):
        self.imaging_subsystem.take_pic()

    def downlink_file(self, pic_name):
        print("Downlinking file")
        if self.power_subsystem.power >= 10:
            self.imaging_subsystem.remove_pic(pic_name)
        else:
            print("Not enough power to tx pic")

    def list_pics(self):
        return self.imaging_subsystem.list_pics() 

    def handle_post(self, command):
        print("Received command {}".format(command)) 


def add_two_things(a, b):
    return a+b

