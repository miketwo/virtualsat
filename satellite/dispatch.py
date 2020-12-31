# -*- coding: utf-8 -*-

class DispatchSubsystem(object):
    def __init__(self):
        super(DispatchSubsystem, self).__init__()
        print("Initilizing Dispatch Subsystem")
        self._SUBSYSTEMS = {}

    def get_tlm(self):
        return {}

    def register_subsystem(self, name, subsystem):
        # Make sure exec function exists
        if subsystem.exec is None:
            raise NotImplementedError("You must implement exec method for processing commands")
        self._SUBSYSTEMS[name] = subsystem

    # def dispatch(self, command):
    #     return self.dispatch(command['subsystem'], command)

    def dispatch(self, subsystem, command):
        if subsystem in self._SUBSYSTEMS:
            return self._SUBSYSTEMS[subsystem].exec(command) 
        else:
            print("ERROR: No subsystem registered to handle '{}'".format(subsystem))
            return False

    def list_register(self):
        print("REGISTRY:")
        cmds = [s for s in self._SUBSYSTEMS]
        for cmd in cmds:
            print("  {}".format(cmd))

