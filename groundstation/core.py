# -*- coding: utf-8 -*-
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pyorbital.orbital import Orbital
import requests
import base64

from groundstation.track import TrackingSystem, NoCurrentPassError


class Groundstation():
    def __init__(self, name, lat, lon):
        super().__init__()
        print("Creating Groundstation")
        self.name = name
        lat = float(lat)
        lon = float(lon)
        self.location = (lat, lon)
        self.tracking_system = TrackingSystem(*self.location)

        self._enabled = True

        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._scheduler.add_job(self.status, 'interval', seconds=5)

        self.sat_url = "http://sat:5001/radio"

    def __str__(self):
        return str(self.status())

    @property
    def target(self):
        return self.tracking_system.target

    def set_target(self, *args, **kwargs):
        self.tracking_system.set_target(*args, **kwargs)
        return self

    def set_enabled(self, enabled_bool):
        self._enabled = enabled_bool

    def status(self):
        status = {
            "name": self.name,
            "time (utc)": datetime.utcnow().timestamp(),
            "enabled": self._enabled,
            "position": self.get_pos(),
            "tracking": self.tracking_system.info(),
        }
        print(status)
        return status

    def get_pos(self):
        return {
            "lat": self.location[0],
            "long": self.location[1],
        }


    ''' Passes a command through to the satellite '''
    def send_command(self, command):
        print("GS | Received command: {}".format(command))
        if self.tracking_system.in_pass():
            print("GS | Sending command to satellite")
            data = {**command, **self.get_pos()}
            res = requests.post(self.sat_url, json=data)
            print(res)
            return res
        else:
            raise NoCurrentPassError("GS | No current pass.")
