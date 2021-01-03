# -*- coding: utf-8 -*-
import base64
import json


class CommunicationSubsystem():
    ''' Fake radio communication '''
    def __init__(self, dispatcher):
        super().__init__()
        self.dispatcher = dispatcher

    def serialize(self, aDict):
        return base64.b64encode(aDict)

    def deserialize(self, aDict):
        # cmd = base64.b64decode(aString)
        # data = json.loads(some_json)
        data = aDict
        if data is None:
        	return
        if not data.get("subsystem"):
            raise SystemError("No subsystem specified for command.")
        print("COMMS | Got command for {}".format(data['subsystem']))
        return self.dispatcher.dispatch(data['subsystem'], command=data)

