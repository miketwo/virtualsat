# -*- coding: utf-8 -*-
from satellite.comms import CommunicationSubsystem
from satellite.dispatch import DispatchSubsystem
from satellite.images import ImagingSubsystem
from satellite.orbit import Orbit
from satellite.power import PowerSubsystem
from satellite.schedule import SchedulerSubsystem
from satellite.telemetry import TelemetrySubsystem


class Satellite(object):

    @classmethod
    def flatsat(cls):
        return cls("FlatSat", None, None)

    def __init__(self, name, tle1, tle2):
        super().__init__()
        self.name = name
        self.tle1 = tle1
        self.tle2 = tle2

        self.flatsat = tle1 is None or tle2 is None

        print("Creating Satellite named {}".format(name))
        print("Please wait...")

        if not self.flatsat:
            self.orbit = Orbit(name, line1=tle1, line2=tle2)

        self._dispatcher = DispatchSubsystem()

        self.power_subsystem = PowerSubsystem()
        self.imaging_subsystem = ImagingSubsystem(self.power_subsystem)

        self._dispatcher.register_subsystem("power", self.power_subsystem)
        self._dispatcher.register_subsystem("image", self.imaging_subsystem)

        self.radio = CommunicationSubsystem(self._dispatcher)

        self._scheduler = SchedulerSubsystem(self._dispatcher)

        self.telemetry_subsystem = TelemetrySubsystem()
        self.telemetry_subsystem.register(self.power_subsystem.get_tlm)
        self.telemetry_subsystem.register(self.imaging_subsystem.get_tlm)
        self.telemetry_subsystem.register(self._scheduler.get_tlm)
        self.telemetry_subsystem.register(self._dispatcher.get_tlm)

        if not self.flatsat:
            self.telemetry_subsystem.register(self.orbit.get_tlm)

        print(self)

    def __str__(self):
        return "\n{}\n{}\n{}".format(self.name, self.tle1, self.tle2)

    def status(self):
        return dict(self.telemetry_subsystem.get_tlm())

    def schedule_command(self, *args, **kwargs):
        self._scheduler.schedule_command(*args, **kwargs)

    def schedule_command_scheduled_pics(self, *args, **kwargs):
        self._scheduler.schedule_command_scheduled_pics(*args, **kwargs)

    def print_commands(self, *args, **kwargs):
        self._scheduler.print_commands(*args, **kwargs)

