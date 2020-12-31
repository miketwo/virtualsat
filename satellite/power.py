# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler

class PowerSubsystem(object):
    MAX_POWER = 100
    DRAIN_RATE = 1
    CHARGE_RATE = 1
    ACTIVITY_POWER_DRAIN = {
        "picture": 5,
        "downlink": 10
    }

    def __init__(self):
        super().__init__()
        print("Initilizing Power Subsystem")
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self._power = self.MAX_POWER
        self._power_mode = 'normal'
        self._reboot_counter = 0
        self.scheduler.add_job(self.update, 'interval', seconds=1)

    def __str__(self):
        return "Mode:{}\tPower:{}\tReboots:{}".format(self._power_mode, self._power, self._reboot_counter)

    @property
    def power(self):
        return self._power

    @property
    def power_mode(self):
        return self._power_mode

    def exec(self, command):
        '''
        Expecting something like:
            {"mode":"recharge|normal"}
        '''
        print("rcvd {}".format(command))
        if "mode" in command.keys():
            return self.set_power_mode(command["mode"])
        else:
            print("Unable to execute command {}".format(command))
            return False

    def get_tlm(self):
        return {
            "mode": self._power_mode,
            "power": self._power,
            "reboots": self._reboot_counter,
        }

    def set_power_mode(self, mode):
        if mode not in ['recharge', 'normal']:
            print("Error: Mode {} not supported.".format(mode))
            return False
        self._power_mode = mode
        return True

    def take_action(self, action):
        self._power -= self.ACTIVITY_POWER_DRAIN[action]

    def update(self):
        if self._power_mode == "recharge" and self._power < self.MAX_POWER:
            self._power += self.CHARGE_RATE
        elif self._power_mode == "normal" and self._power > 0:
            self._power -= self.DRAIN_RATE
        else:
            None

        # Reset if out of power
        if self._power <= 0:
            self.set_power_mode('recharge')
            self._reboot_counter += 1

        