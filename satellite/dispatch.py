# -*- coding: utf-8 -*-
import logging
from pydispatch import dispatcher

logger = logging.getLogger(__name__)

class DispatchSubsystem(object):
    def __init__(self):
        super(DispatchSubsystem, self).__init__()
        logger.info("Initilizing Dispatch Subsystem")
        self._SUBSYSTEMS = {}

    def get_tlm(self):
        return {}

    def register_subsystem(self, name, subsystem):
        # Make sure exec function exists
        if subsystem.exec is None:
            raise NotImplementedError("You must implement exec method for processing commands")
        # self._SUBSYSTEMS[name] = subsystem
        return dispatcher.connect(subsystem.exec, signal=name, sender=dispatcher.Any)

    def dispatch(self, subsystem, command):
        # if subsystem in self._SUBSYSTEMS:
        #     return self._SUBSYSTEMS[subsystem].exec(command)
        # else:
        #     errmsg = "ERROR: No subsystem registered to handle '{}'".format(subsystem)
        #     raise SystemError(errmsg)
        return dispatcher.send(signal=subsystem, sender=self, command=command)

