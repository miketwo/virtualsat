# -*- coding: utf-8 -*-
import logging
from pydispatch import dispatcher

logger = logging.getLogger(__name__)

class DispatchSubsystem():
    def __init__(self):
        super(DispatchSubsystem, self).__init__()
        logger.info("Initilizing Dispatch Subsystem")
        self._SUBSYSTEMS = set()

    def get_tlm(self):
        return {"dispatch": {
            "registered subs": list(self._SUBSYSTEMS)
        }}

    def register_subsystem(self, name, subsystem):
        # Make sure exec function exists
        if subsystem is None:
            raise NotImplementedError("You must implement exec method for processing commands")
        self._SUBSYSTEMS.add(name)
        return dispatcher.connect(subsystem, signal=name, sender=dispatcher.Any)

    def dispatch(self, subsystem, command):
        # if subsystem in self._SUBSYSTEMS:
        #     return self._SUBSYSTEMS[subsystem].exec(command)
        # else:
        #     errmsg = "ERROR: No subsystem registered to handle '{}'".format(subsystem)
        #     raise SystemError(errmsg)
        print("DISPATCH | Sending command to {}".format(subsystem))
        return dispatcher.send(signal=subsystem, sender=self, command=command)

