# -*- coding: utf-8 -*-
from datetime import timedelta
from functools import partial, partialmethod

from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerSubsystem(object):
    def __init__(self, dispatcher):
        super().__init__()
        print("Initilizing Scheduler Subsystem")
        self._command_id = 1
        self._dispatcher = dispatcher

        self.command_scheduler = BackgroundScheduler()
        self.command_scheduler.start()

    def get_tlm(self):
        return {
            "num scheduled commands": len(self.get_commands()),
            "scheduled commands": self.get_commands()
        }

    def schedule_command(self, subsystem, command, target_datetime):
        tmp = str(self._command_id)
        name = "CMD #{}: {} | {} at {}".format(tmp, subsystem, command, target_datetime)
        func = partial(self._dispatcher.dispatch, subsystem, command)
        self.command_scheduler.add_job(func, 'date', run_date=target_datetime, id=tmp, name=name)
        # print("  Scheduled command {} at {}".format(tmp, target_datetime))
        self._command_id += 1
        return tmp

    def remove_command(self, command_id):
        self.command_scheduler.remove_job(command_id)

    def clear_commands(self):
        cmds = [j.id for j in self.command_scheduler.get_jobs()]
        for cmd in cmds:
            self.command_scheduler.remove_job(cmd)

    def get_commands(self):
        cmds = [j.name for j in self.command_scheduler.get_jobs()]
        return cmds

    def print_commands(self):
        print("SCHEDULED COMMANDS:")
        cmds = [j.name for j in self.command_scheduler.get_jobs()]
        for cmd in cmds:
            print("  {}".format(cmd))

    def schedule_command_scheduled_pics(self, start_date, duration_sec):
        tmp = str(self._command_id)
        subsystem = "image"
        command = {"pic": "CREATE"}
        name = "CMD #{}: {} | Picture Window @ {} for {} seconds".format(tmp, subsystem, start_date, duration_sec)
        func = partial(self._dispatcher.dispatch, subsystem, command)
        self.command_scheduler.add_job(
            func,
            'interval', 
            seconds=5, 
            start_date=start_date, 
            end_date=start_date+timedelta(seconds=duration_sec),
            id=tmp,
            name=name)
        # print("Scheduled command {} at {} for {} seconds".format(tmp, start_date, duration_sec))
        self._command_id += 1
        return tmp