# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from pyorbital.orbital import Orbital
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class TrackingError(SystemError):
    pass

class NoCurrentPassError(SystemError):
    pass


class TrackingSystem():
    _DT_FOR_TEST = None

    def __init__(self, gs_lat, gs_long):
        super().__init__()
        ("Creating TrackingSystem")
        self.azimuth = 0
        self.elevation = 0
        self.location = (float(gs_lat), float(gs_long))

        self.target = None

        self._scheduler = BackgroundScheduler()
        self._scheduler.start()

        self._next_passes = []

        self._scheduler.add_job(self._recalc_pointing, 'interval', seconds=1)
        self._scheduler.add_job(self._recalc_passes, 'interval',  minutes=10)

    def now(self):
        return datetime.utcnow() if self._DT_FOR_TEST is None else self._DT_FOR_TEST

    def returns_true(self):
        return True

    def in_pass(self):
        res = self.tracking() and self.target_in_view()
        return bool(res)

    def set_target(self, name, line1, line2):
        self.target = Orbital(name, line1=line1, line2=line2)
        self._recalc_passes()
        self._recalc_pointing()
        return self

    def clear_target(self):
        self.target = None
        self._next_passes = []

    def get_passes(self):
        if self.target is None:
            return []
        else:
            HOURS_TO_CHECK = 12
            # returns a list of [(risetime, falltime, highest)]
            passes = self.target.get_next_passes(
                utc_time=self.now(),
                length=HOURS_TO_CHECK,
                lat=self.location[0],
                lon=self.location[1],
                alt=0)
            return passes

    def tracking(self):
        return self.target is not None

    def target_in_view(self):
        if self.target is None:
            return False
        else:
            az, el = self._get_az_el()
            return bool(el > 0)

    def get_current_pass(self):
        try:
            # Find pass with rise time in the past and fall time in the future
            for p in self._next_passes:
                rise, fall, high = p
            return next(x for x in self._next_passes if x[0] < self.now() and x[1] > self.now())
        except StopIteration:
            # No current pass
            return None

    def get_next_pass(self):
        try:
            # Find next pass that hasn't started yet
            return next(x for x in self._next_passes if x[0] > self.now())
        except StopIteration:
            # No upcoming passes
            return None

    def _info_pass(self, a_pass, title):
        rise, fall, high = a_pass
        tmp = {title: {
            "absolute": {
                "rise time": rise.isoformat(),#strftime("%m/%d %H:%M:%S"),
                "fall time": fall.isoformat(),#strftime("%m/%d %H:%M:%S"),
                "highest": high.isoformat(),#strftime("%m/%d %H:%M:%S"),
            },
            "relative (sec)": {
                "rise time": (rise - self.now()).total_seconds(),
                "fall time": (fall - self.now()).total_seconds(),
                "highest": (high - self.now()).total_seconds(),
            }
        }}
        return tmp

    def info_next_pass(self):
        next_pass = self.get_next_pass()
        if next_pass:
            return self._info_pass(next_pass, "next_pass")
        return {}

    def info_current_pass(self):
        current_pass = self.get_current_pass()
        if current_pass:
            return self._info_pass(current_pass, "current_pass")
        return {}

    def info(self):
        tmp = {
            "utc_time": self.now().timestamp(),
            "azimuth": self.azimuth,
            "elevation": self.elevation,
            "tracking": self.tracking(),
            "in_pass": self.in_pass(),
        }
        tmp = {**tmp, **self.info_next_pass(), **self.info_current_pass()}
        return tmp

    def _recalc_passes(self):
        if self.target is not None:
            self._next_passes = self.get_passes()

    def _recalc_pointing(self):
        ("{},{},{}".format(self.now(), *self.location))
        if self.target is not None:
            az, el = self._get_az_el()
            if el < 0:
                el = 0
            self.azimuth, self.elevation = az, el
            return (self.azimuth, self.elevation)
        else:
            self.elevation = 0
            return None

    def _get_az_el(self):
        az, el = self.target.get_observer_look(
                utc_time=self.now(),
                lat=self.location[0],
                lon=self.location[1],
                alt=0)
        return (az, el)

