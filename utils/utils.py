#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from satellite.core import Satellite
from pyorbital import tlefile


def create_sat_from_env():
    ''' Creates a satellite from environment variables
    The satellite will be orbiting if ORBIT=TRUE.
    Otherwise the satellite will act as a FlatSat.
    '''
    if os.getenv("ORBIT", "FALSE") == "TRUE":
        for envar in ["SATNAME", "TLE1", "TLE2"]:
            if os.getenv(envar) is None:
                raise NameError("{} must be specified as an environment variable.".format(envar))

        satname = os.getenv('SATNAME')
        tle1 = os.getenv('TLE1')
        tle2 = os.getenv('TLE2')
        return Satellite(satname, tle1, tle2)
    else:
        return Satellite.flatsat()


def create_random_sat():
    import random
    raw_data = read_satfile()
    sats = parse_tles(raw_data)
    print("Number of satellites : {}".format(len(sats)))
    selected_sat = random.choice(sats)
    return Satellite(selected_sat.platform, selected_sat.line1, selected_sat.line2)


def parse_tles(raw_data):
    """Parse all the TLEs in the given raw text data."""
    tles = []
    line1, line2 = None, None
    raw_data = raw_data.split('\n')
    for row in raw_data:
        if row.startswith('1 '):
            line1 = row
        elif row.startswith('2 '):
            line2 = row
        else:
            name = row
        if line1 is not None and line2 is not None:
            try:
                tle = tlefile.Tle(name, line1=line1, line2=line2)
            except ValueError:
                logging.warning(
                    "Invalid data found - line1: %s, line2: %s",
                    line1, line2)
            else:
                tles.append(tle)
            line1, line2 = None, None
    return tles

# Hack to get Starlink sats loaded.
def read_satfile():
    filepath = "/app/starlink.txt"
    with open(filepath, 'r') as content_file:
        content = content_file.read()
    return content

