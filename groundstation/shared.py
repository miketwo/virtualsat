from multiprocessing import Lock
from multiprocessing.managers import BaseManager

class SharedState:
    def __init__(self, address, authkey):
        self._data = {}
        self._lock = Lock()
        self._manager = BaseManager(address, authkey)
        self._manager.register('get', self._get)
        self._manager.register('set', self._set)
        try:
            self._manager.get_server()
            self._manager.start()
        except OSError: # Address already in use
            self._manager.connect()
    def __getattr__(self, name):
        if name.startswith('_'):
            return object.__getattr__(self, name)
        return self._manager.get(name)._getvalue()
    def __setattr__(self, name, value):
        if name.startswith('_'):
            return object.__setattr__(self, name, value)
        return self._manager.set(name, value)
    def _get(self, name):
        return self._data[name]
    def _set(self, name, value):
        with self._lock:
            self._data[name] = value