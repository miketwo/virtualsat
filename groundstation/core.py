# -*- coding: utf-8 -*-
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pyorbital.orbital import Orbital
import requests
import base64

class Groundstation():
    '''
    Simple groundstation:
     - It has a location (lat/long)
     - It has a tracking antenna that can track orbital objects
    (Future)
     - It can be enabled/disabled for maintanence
       - The need for maintanence builds over time
     - It generates telemetry
    '''
    def __init__(self, name, lat, lon):
        super().__init__()
        print("Creating Groundstation")
        self.name = name
        self.location = (lat, lon)
        self._az = 0
        self._el = 0
        self._target = None
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._enabled = True
        self._scheduler.add_job(self.status, 'interval', seconds=5)
        self._scheduler.add_job(self.update, 'interval', seconds=1)
        self.sat_url = "http://0.0.0.0:5001/radio"

    def __str__(self):
        return str(self.status())

    @property
    def target(self):
        return self._target
    
    def set_target(self, name, line1, line2):
        self._target = Orbital(name, line1=line1, line2=line2)

    def set_enabled(self, enabled_bool):
        self._enabled = enabled_bool

    def status(self):
        status = {
            "name": self.name,
            "time": datetime.utcnow().timestamp(),
            "enabled": self._enabled,
            **self.get_pos(),
            **self.get_pointing(),
        }
        print(status)

        cmd = {
            "subsystem": "power",
            "mode": "recharge"
        }
        self.send_command(cmd)

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
        data = {**command, **self.get_pos()}
        # payload = {"radio": base64.b64encode(data) }
        res = requests.post(self.sat_url, data=data)
        print(res)

