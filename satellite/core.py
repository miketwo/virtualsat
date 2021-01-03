# -*- coding: utf-8 -*-
from satellite.comms import CommunicationSubsystem
from satellite.dispatch import DispatchSubsystem
from satellite.value import ValueSubsystem
from satellite.orbit import Orbit
from satellite.power import PowerSubsystem
from satellite.schedule import SchedulerSubsystem
from satellite.telemetry import TelemetrySubsystem


class Satellite():

    @classmethod
    def flatsat(cls):
        return cls("FlatSat", None, None)

    def __init__(self, name, tle1, tle2):
        super().__init__()
        self.name = name
        self.tle1 = tle1
        self.tle2 = tle2

        self.flatsatmode = tle1 is None or tle2 is None

        print("Creating Satellite named {}".format(name))

        # Create all subsystems
        self._dispatcher = DispatchSubsystem()
        self.power_subsystem = PowerSubsystem()
        self.value_subsystem = ValueSubsystem(self.power_subsystem)
        self._scheduler = SchedulerSubsystem(self._dispatcher)
        self.radio = CommunicationSubsystem(self._dispatcher)
        if not self.flatsatmode:
            self.orbit = Orbit(name, line1=tle1, line2=tle2)

        # Wire things up...
        self._dispatcher.register_subsystem("power", self.power_subsystem.exec)
        self._dispatcher.register_subsystem("value", self.value_subsystem.exec)
        self._dispatcher.register_subsystem("sched", self._scheduler.exec)

        self.telemetry_subsystem = TelemetrySubsystem()
        self.telemetry_subsystem.register(self.power_subsystem.get_tlm)
        self.telemetry_subsystem.register(self.value_subsystem.get_tlm)
        self.telemetry_subsystem.register(self._scheduler.get_tlm)
        self.telemetry_subsystem.register(self._dispatcher.get_tlm)

        if not self.flatsatmode:
            self.telemetry_subsystem.register(self.orbit.get_tlm)

        print(self)

    def __str__(self):
        return "\n{}\n{}\n{}".format(self.name, self.tle1, self.tle2)

    def status(self):
        return dict(self.telemetry_subsystem.get_tlm())

