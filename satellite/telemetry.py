# -*- coding: utf-8 -*-
from datetime import datetime
import collections
from apscheduler.schedulers.background import BackgroundScheduler


class TelemetrySubsystem(object):
    TLM_MAX_HISTORY = 10
    RECORD_FREQ_SEC = 1

    def __init__(self):
        super(TelemetrySubsystem, self).__init__()
        print("Initilizing Telemetry Subsystem")
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._registry = set()
        self._tlm_history = collections.deque(maxlen=self.TLM_MAX_HISTORY)
        self._tlm_idx = 0
        self.register(self.time)
        self._scheduler.add_job(self.record_tlm, 'interval', seconds=self.RECORD_FREQ_SEC)

    def register(self, subsystem_tlm_method):
        '''Registers a subsystem with Telemetry.
        You must provide a function to call. This function must return
        a dictionary of key-value pairs of telemetry.
        '''
        self._registry.add(subsystem_tlm_method)

    def exec(self, command):
        '''
        Respond to any command with current telemetry
        '''
        logger.debug("rcvd {}".format(command))
        return get_tlm()

    def __str__(self):
        return str(self.get_tlm())

    def time(self):
        return {"time": datetime.utcnow().timestamp() }

    def get_tlm(self):
        dicts = [func() for func in self._registry]
        merged = {k: v for d in dicts for k, v in d.items()}
        return merged

    def get_history(self):
        return list(self._tlm_history)[::-1]   # Reversed from the deque order

    def record_tlm(self):
        self._tlm_history.append(self.get_tlm())
