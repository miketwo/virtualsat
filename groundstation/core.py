# -*- coding: utf-8 -*-
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pyorbital.orbital import Orbital
import requests
import base64


class TrackingError(SystemError):
    pass


class Groundstation():
    def __init__(self, name, lat, lon):
        super().__init__()
        print("Creating Groundstation")
        self.name = name
        lat = float(lat)
        lon = float(lon)
        self.location = (lat, lon)
        self._az = 0
        self._el = 0
        self._target = None
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._enabled = True
        self._next_passes = []
        self._scheduler.add_job(self.status, 'interval', seconds=5)
        self._scheduler.add_job(self.update_antenna, 'interval', seconds=1)
        self._scheduler.add_job(self.recalc_passes, 'interval',  minutes=10)
        self.sat_url = "http://sat:5001/radio"

        # For quick testing...
        # TLE1 ="1 44238U 19029D   20366.78684316  .00004289  00000-0  24662-3 0  9998"
        # TLE2 ="2 44238  52.9975  32.3246 0001305  89.7284 270.3857 15.14479195 87325"
        # self.set_target("blah", TLE1, TLE2)

    def __str__(self):
        return str(self.status())

    @property
    def target(self):
        return self._target

    def set_target(self, name, line1, line2):
        self._target = Orbital(name, line1=line1, line2=line2)
        self.recalc_passes()

    def clear_target(self):
        self._target = None

    def get_passes(self):
        if self._target is None:
            raise TrackingError("No satellite being tracked.")
        else:
            HOURS_TO_CHECK = 12
            # returns a list of [(risetime, falltime, highest)]
            passes = self._target.get_next_passes(
                utc_time=datetime.utcnow(),
                length=HOURS_TO_CHECK,
                lon=self.location[1],
                lat=self.location[0],
                alt=0)
            return passes

    def recalc_passes(self):
        if self._target is None:
            return
        self._next_passes = self.get_passes()

    def set_enabled(self, enabled_bool):
        self._enabled = enabled_bool

    def status(self):
        status = {
            "name": self.name,
            "time (utc)": datetime.utcnow().timestamp(),
            "enabled": self._enabled,
            "position": self.get_pos(),
            "tracking": self.get_pointing(),
        }
        print(status)
        return status

    def update_antenna(self):
        ("{},{},{}".format(datetime.utcnow(),*self.location))
        if self.target is not None:
            az, el = self.target.get_observer_look(datetime.utcnow(),*self.location,0)
            if el > 0:
                el = 0
            self._az, self.el = az, el

    def target_in_view(self):
        if self._target is None:
            raise TrackingError("No satellite being tracked.")
        else:
            az, el = self.target.get_observer_look(datetime.utcnow(),*self.location,0)
            return el > 0

    def get_pos(self):
        return {
            "lat": self.location[0],
            "long": self.location[1],
        }

    def get_pointing(self):
        tmp = {
            "azimuth": self._az,
            "elevation": self._el,
            "tracking": self.target is not None,
            "in pass": self._el > 0,
        }
        if self._next_passes:
            rise,fall,high = self._next_passes[0]
            tmp = {**tmp, "next pass": {
                "absolute": {
                    "rise time": rise.strftime("%m/%d %H:%M:%S"),
                    "fall time": fall.strftime("%m/%d %H:%M:%S"),
                    "highest": high.strftime("%m/%d %H:%M:%S"),
                },
                "relative": {
                    "rise time": str(rise - datetime.utcnow()),
                    "fall time": str(fall - datetime.utcnow()),
                    "highest": str(high - datetime.utcnow()),
                }
            }}
        return tmp


    ''' Passes a command through to the satellite '''
    def send_command(self, command):
        print("GS | Received command: {}".format(command))
        if self.target is None:
            raise TrackingError("No satellite being tracked.")
        if not self.target_in_view():
            raise TrackingError("Satellite is not visible.")
        data = {**command, **self.get_pos()}
        res = requests.post(self.sat_url, json=data)
        print(res)
        return res

