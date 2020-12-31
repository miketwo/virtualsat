# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta

class CommandSubsystem(object):
    def __init__(self):
        super(CommandSubsystem, self).__init__()
        print("Initilizing Command Subsystem")
        self._command_id = 1
        self._COMMANDS = {}

        self.command_scheduler = BackgroundScheduler()
        self.command_scheduler.start()

    def get_tlm():
        return {}

    def register_command(self, name, func):
        self._COMMANDS[name] = func

    def run_command(self, command):
        self._COMMANDS[command]()        

    def add_command(self, command, target_datetime):
        tmp = str(self._command_id)
        name = "CMD #{}: {}".format(tmp, command)
        self.command_scheduler.add_job(self._COMMANDS[command], 'date', run_date=target_datetime, id=tmp, name=name)
        print("Added command {}".format(tmp))
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
        print("COMMANDS:")
        cmds = [j.name for j in self.command_scheduler.get_jobs()]
        for cmd in cmds:
            print("  {}".format(cmd))

    def add_command_scheduled_pics(self, start_date, duration_sec):
        tmp = str(self._command_id)
        name = "CMD #{}: Picture Window @ {} for {} seconds".format(tmp, start_date, duration_sec)
        self.command_scheduler.add_job(
            self._COMMANDS['take_pic'],
            'interval', 
            seconds=5, 
            start_date=start_date, 
            end_date=start_date+timedelta(seconds=duration_sec),
            id=tmp,
            name=name)
        print("Added command {}".format(tmp))
        self._command_id += 1
        return tmp