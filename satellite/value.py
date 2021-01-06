# -*- coding: utf-8 -*-
import collections
from pydispatch import dispatcher
from functools import partial

# debug listener, prints sender and params
def debug_listener(sender, **kwargs):
    print("[DEBUG] '{}' sent data '{}'".format(
        sender,
        ", ".join([
            "{} => {}".format(key, value) for key, value in kwargs.items()
        ]))
    )
quickconnect = partial(
    dispatcher.connect,
    signal="GLOBAL",
    sender=dispatcher.Any)
quickconnect(debug_listener)


class ValueSubsystem():
    MAX_VALUE = 10000

    def __init__(self, power_subsystem):
        super().__init__()
        print("Initilizing Value Subsystem")
        self.pwr = power_subsystem
        self._value = collections.deque(maxlen=self.MAX_VALUE)
        self._value_counter = 1
        self._download_counter = 0
        self._lost_counter = 0
        quickconnect(self.handle_signals)

    @property
    def value(self):
        return list(self._value)

    def handle_signals(self, msg):
        if "reboot" in msg:
            self.reboot_clear()

    def exec(self, command):
        '''
        Expecting something like:
            {"value":"create"}
            {"value":"download"}
            {"value":"clear"}
        '''
        cmdlist = {
                "create": self.create_value,
                "download": self.download,
                "clear": self.clear
        }
        if "value" in command.keys():
            cmdlist[command["value"]]()
        else:
            errmsg = "Unable to execute command {}".format(command)
            raise ValueError(errmsg)
        return True

    def clear(self):
        self._value.clear()

    def reboot_clear(self):
        self._lost_counter += len(self._value)
        self.clear()

    def download(self):
        if self.pwr.mode != "normal":
            errmsg = "ERROR: Must be in normal power mode to download value"
            raise SystemError(errmsg)
        if len(self._value) == 0:
            errmsg = "ERROR: No value to download"
            raise SystemError(errmsg)
        self.pwr.take_action('value')
        self._value.pop()
        self._download_counter += 1

    def create_value(self):
        if self.pwr.mode != "normal":
            errmsg = "ERROR: Must be in normal power mode to create value"
            raise SystemError(errmsg)
        self.pwr.take_action('value')
        name = "Value{}".format(self._value_counter)
        if len(self._value) == self.MAX_VALUE:
            print("Overwriting previous...")
            self._lost_counter += 1
        self._value.append(name)
        self._value_counter += 1
        return self.get_tlm()

    def get_tlm(self):
        return {
            "value": {
                "num": len(self.value),
                "names": self.value,
                "num_downloaded": self._download_counter,
                "num_lost": self._lost_counter
            }
        }
