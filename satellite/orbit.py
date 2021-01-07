from pyorbital.orbital import Orbital
from datetime import datetime


class Orbit(Orbital):
    def __init__(self, name, line1, line2):
        super().__init__(name, line1=line1, line2=line2)

    def get_tlm(self):
        lon, lat, alt = self.current_position()
        return {"position": {
            "latitude": lat,
            "longitude": lon,
            "altitude (km)": alt
        }}

    def current_position(self):
        return self.get_lonlatalt(datetime.utcnow())

    def get_look(self, lat, lon):
        return self.get_observer_look(datetime.utcnow(), lat, lon, 0)

    def is_visible_from(self, lat,lon):
        az, el = self.get_look(lat, lon)
        return el > 0
