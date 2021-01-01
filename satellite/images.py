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


class ImagingSubsystem(object):
    MAX_PICS = 10

    def __init__(self, power_subsystem):
        super().__init__()
        print("Initilizing Image Subsystem")
        self.pwr = power_subsystem
        self._pictures = collections.deque(maxlen=self.MAX_PICS)
        self._pic_counter = 1
        self._download_counter = 0
        self._lost_counter = 0
        quickconnect(self.handle_signals)

    @property
    def pictures(self):
        return list(self._pictures)

    def handle_signals(self, msg):
        if "reboot" in msg:
            self.reboot_clear()

    def exec(self, command):
        '''
        Expecting something like:
            {"image":"take"}
            {"image":"download"}
            {"image":"clear"}
        '''
        cmdlist = {
                "take": self.take_pic,
                "download": self.download,
                "clear": self.clear
        }
        if "image" in command.keys():
            cmdlist[command["image"]]()
        else:
            errmsg = "Unable to execute command {}".format(command)
            raise ValueError(errmsg)
        return True

    def clear(self):
        self._pictures.clear()

    def reboot_clear(self):
        self._lost_counter += len(self._pictures)
        self.clear()

    def download(self):
        if self.pwr.mode != "normal":
            errmsg = "ERROR: Must be in normal power mode to download pictures"
            raise SystemError(errmsg)
        try:
            self.pwr.take_action('picture')
            self._pictures.pop()
            self._download_counter += 1
        except IndexError:
            errmsg = "ERROR: No pictures to download"
            raise SystemError(errmsg)

    def take_pic(self):
        if self.pwr.mode != "normal":
            errmsg = "ERROR: Must be in normal power mode to take pictures"
            raise SystemError(errmsg)
        self.pwr.take_action('picture')
        picname = "Pic{}".format(self._pic_counter)
        self._pictures.append(picname)
        self._pic_counter += 1
        return self.get_tlm()

    def get_tlm(self):
        return {
            "num_pictures": len(self.pictures),
            "pictures": self.pictures,
            "num_downloaded": self._download_counter,
            "num_lost": self._lost_counter
        }
