# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from functools import partial, partialmethod

from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerSubsystem():
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

    def exec(self, command):
        '''
        Expecting something like:
            {
            "time": (utc timestamp)
            "command": {
                "subsystem": "power"
                "mode": "r"
                }
            }
        '''
        print("SCHEDULER | Processing command")
        if "time" in command and "command" in command:
            subsystem = command["command"]["subsystem"]
            subcommand = command["command"]
            target_datetime = datetime.utcfromtimestamp(int(float((command["time"]))))
            self.schedule_command(subsystem, subcommand, target_datetime)
            return self.get_tlm()
        else:
            errmsg = "SCHEDULER | Unable to execute command {}".format(command)
            raise ValueError(errmsg)

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
