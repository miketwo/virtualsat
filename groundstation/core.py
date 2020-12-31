# -*- coding: utf-8 -*-
import sched
import random
import time
import json
from datetime import datetime, timedelta
from functools import partial, partialmethod
from apscheduler.schedulers.background import BackgroundScheduler
from pyorbital.orbital import Orbital
import requests

'''
Simple groundstation:
 - It has a location (lat/long)
(Future)
 - It has a tracking antenna that can track orbital objects
 - It can be enabled/disabled for maintanence
   - The need for maintanence builds over time
 - It generates telemetry
'''
class Groundstation():
    def __init__(self, name, lat, lon):
        super(Groundstation, self).__init__()
        print("Creating Groundstation")
        self.name = name
        self.location = (lat, lon)
        self._az = 0
        self._el = 0
        self._target = None
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._scheduler.add_job(self.status, 'interval', seconds=5)
        self._scheduler.add_job(self.update, 'interval', seconds=1)
        self.sat_url = "localhost:5000/sat"

    def __str__(self):
        return str(self.status())

    @property
    def target(self):
        return self._target
    
    def set_target(self, name, line1, line2):
        self._target = Orbital(name, line1=line1, line2=line2)

    def status(self):
        status = {
            "name": self.name,
            "time": datetime.utcnow().timestamp(),
            **self.get_pos(),
            **self.get_pointing(),
        }
        print(status)
        return status

    def update(self):
        if self.target is not None:
            az, el = self.target.get_observer_look(datetime.now(),*self.location,0)
            if el > 0:
                el = 0
            self._az, self.el = az, el

    def get_pos(self):
        return {
            "lat": self.location[0],
            "long": self.location[1],
        }

    def get_pointing(self):
        return {
            "azimuth": self._az,
            "elevation": self._el,
            "tracking": self.target is not None,
            "in pass": self._el > 0,
        }

    def send_command(self, command):
        data = {}.update(command, self.get_pos())
        res = requests.post(self.sat_url, data=data)
        print(res)


