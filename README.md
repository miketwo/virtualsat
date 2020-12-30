# Virtual Satellite

## Getting Started

Run main.py. Command the satellite with 1-letter commands.

ToDo:
 - API interface


## Design Principles

### STAY SIMPLE: 
 - Operator must balance imaging, downlinking, and recharging.
 
 - We must correctly simulate communication over a groundstation. The groundstation's lat/long can be included with each API call. That is used to determine if comms is possible. 

## Program properties

State:
  - Storage, Power, Position/Orbit, Command schedule, Telemetry History?

Automatic:
  - Telemetry is generated every XX seconds
    -- There is a maximum amount that can be stored
    -- Old telemetry is overwritten as newer stuff is added
  - Power is gained/reduced every XX seconds
    -- It costs power to take pics
    -- Reaching 0 power causes a reboot. Lose all Pics and enter "safe mode" (recharging mode).


Imaging Commands: 
  - Take pictures (straight down at current lat/long -- populate from Google Earth?)
  - Pics are taken on a commanded window
    -- Start time + duration
    -- It costs power to take pics
    -- There is a maximum amount that can be stored. Asking for more produces errors.

Power Commands: 
  - It takes power to take downlink. Max battery XX Watt-hours. It takes 10 orbits to fully charge.
  - Recharge Mode
  - Normal Mode

Comm Commands: 
  - Downlink pics
  - Downlink speed artificially limits to XX/2 per pass (i.e. It takes 2 passes to drain the storage entirely)
  - Downlink telemetry (live or historical)

Schedule:
  - Schedule a command (time, command)
  - Cancel a scheduled command


## Other notes

3rd Party?
- There was a VirtualSat SBIR in 1998: https://sbir.nasa.gov/SBIR/abstracts/98/sbir/phase1/SBIR-98-1-13.11-5300.html
- The Hammers Company made it: https://hammers.com/virtualsat
- Not sure if we/they would be intersted in partnering?
- Could be WAAY too high fidelity. The point is to demo Major Tom, not get lost in satellite functionality...