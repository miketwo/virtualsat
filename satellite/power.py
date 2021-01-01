# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from pydispatch import dispatcher

import logging
logger = logging.getLogger(__name__)

class PowerSubsystem(object):
    MAX_POWER = 100
    MIN_POWER = 0
    DRAIN_RATE = 1
    CHARGE_RATE = 1
    ACTIVITY_POWER_DRAIN = {
        "picture": 5,
        "download": 10
    }

    def __init__(self, **kwargs):
        super().__init__()
        logger.info("Initilizing Power Subsystem")
        self.scheduler = kwargs.get("scheduler", BackgroundScheduler())
        self.scheduler.start()
        self._power = self.MAX_POWER
        self._mode = 'normal'
        self._reboot_counter = 0
        self.scheduler.add_job(self.update, 'interval', seconds=1)
        dispatcher.connect(self.exec, signal="COMMANDS", sender=dispatcher.Any)

    def __str__(self):
        return "Mode:{}\tPower:{}\tReboots:{}".format(self._mode, self._power, self._reboot_counter)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        if value > self.MAX_POWER:
            self._power = self.MAX_POWER
        elif value < self.MIN_POWER:
            self._power = self.MIN_POWER
        else:
            self._power = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in ['recharge', 'normal']:
            errmsg = "Mode {} not supported.".format(value)
            raise ValueError(errmsg)
        self._mode = value

    def configure(self, config):
        self.power = config.get("power", self.power)
        self.mode = config.get("mode", self.mode)
        self._reboot_counter = config.get("reboots", self._reboot_counter)

    def exec(self, command):
        '''
        Expecting something like:
            {"mode":"recharge|normal"}
        '''
        logger.debug("rcvd {}".format(command))
        if "mode" in command.keys():
            self.mode = command["mode"]
            return self.get_tlm()
        else:
            errmsg = "Unable to execute command {}".format(command)
            raise ValueError(errmsg)

    def get_tlm(self):
        return {
            "mode": self._mode,
            "power": self._power,
            "reboots": self._reboot_counter,
        }

    def take_action(self, action):
        if action not in self.ACTIVITY_POWER_DRAIN:
            raise SystemError("Action not supported")
        if self.ACTIVITY_POWER_DRAIN[action] > self.power:
            errmsg = "Not enough power to do: {}".format(action)
            raise SystemError(errmsg)
        self.power -= self.ACTIVITY_POWER_DRAIN[action]
        return self.get_tlm()

    def update(self):
        if self._mode == "recharge" and self.power < self.MAX_POWER:
            self.power += self.CHARGE_RATE
        elif self._mode == "normal" and self.power > 0:
            self.power -= self.DRAIN_RATE
        else:
            None

        # Reset if out of power
        if self.power <= 0:
            self.power = 0
            self.mode = 'recharge'
            self._reboot_counter += 1
            dispatcher.send(signal="GLOBAL", sender=self, msg="reboot")

        return self.get_tlm()
        