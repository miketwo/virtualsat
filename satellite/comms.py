# -*- coding: utf-8 -*-
import base64
import json

class CommunicationSubsystem(object):
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
        print("Got command: {}".format(data))
        if data is None:
        	return
        return self.dispatcher.dispatch(data['subsystem'], data)
