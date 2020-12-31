# Virtual Satellite

- Launch the satellite and go to localhost:PORT/debug to see the satellite status and TLEs

Level 1: Flatsat
- Play with the satellite using the commands and buttons on debug. (Or MT interactive mode). Notice how power charges/discharges. Notice how pictures can be taken. Notice how if you run out of power, you lose all pictures. Notice how telemetry is created. Downlink as many pictures as you can.

Level 2: Orbit
- Now you need to schedule all your commands, using MT. Add the satellite to MT
- Add a Groundstation (need to dockerize this as well)
- Add a Gateway (?)
- Schedule commands and downlink as many pictures as you can. 

Level 3: Tbd... (more realism? manage thermal + other subsystems)



## Quicktart
Run `launchsat.sh`. Command the satellite with 1-letter commands:
 - 'r' to recharge
 - 'n' for normal mode
 - 'p' for pics
 - 'l' for list pics
 - 'd' for download pic

### Commands


#### Satellite
- Power
 - "p r" - power recharge
 - "p n" - power normal
- Images
 - "i SEC" - take images for SEC seconds.
 - "i d #" - downlink image #
- Telemetry
 - "t d" - download all telemetry
- Scheduling
 - "s START_TIME CMD"

#### Groundstation
- Tracking
 - "t ????" -- track sat (TBD)
- Maintanence
 - "e 0|1" -- enable GS | Maintainance mode
- Commanding
 - "f CMD" -- forward CMD to sat

ToDo:
 - API interface
 - Logging instead of prints
 - Make docker work. Publish to registry.
 - Interactive flatsat mode that ignores GS location?


## Design Principles

### STAY SIMPLE: 
 - Operator must balance Imaging, Downlinking, and Recharging.
 
 - We must correctly simulate communication over a groundstation. The groundstation's lat/long can be included with each API call. That is used to determine if comms is possible. 

 - We must communicate with the satellite over a json API, not programmatically. The satellite code should be a black box.

 - The groundstation must be extremely simple. Just adds its own location to the commands.

 - It would be nice if they were each containers that talked to each other. It would also be nice if the GS and Satellite have no idea what Major Tom is, to better simulate interfacing with 3rd party systems.

 - We need to connect to Major Tom (Gateway to GS?)


## Program properties
The satellite keeps track of the following state:
  - Onboard Storage, including
    - Telemetry history
    - Picture history
  - Power, including
    - "Mode" (recharging vs not)
    - Number of Reboots
  - Position/Orbit
  - Command schedule

### Telemetry Subsystem
  - Telemetry is generated every XX seconds
    - There is a maximum amount that can be stored
    - Old telemetry is overwritten as newer stuff is added

### Power Subsystem
 - Power is gained/reduced every XX seconds
   - It costs extra power to take pics
   - It costs extra power to downlink pics
   - Reaching 0 power causes a reboot. Sat automatically switches to "recharge mode" 
 - It takes XX orbits to recharge fully.

### Communication Subsystem
  - Upload commands (scheduled or immediate)
  - Downlink pics
    - Downlink speed artificially limited (it takes 2 passes to drain storage)
  - Downlink telemetry
    - All TLM can be downloaded instantaneously

### Scheduling Subsystem
  - Schedule a command (time, command)
  - Cancel a scheduled command

### Imaging Subsystem
  - Take pictures (straight down at current lat/long -- populate from Google Earth?)
  - Pics are taken on a commanded window
    -- Start time + duration
    -- It costs power to take pics
    -- There is a maximum amount that can be stored. Asking for more produces errors.
    -- Minimum window duration is enforced
    -- Overlapping window are not allowed


## Other notes

3rd Party?
- There was a VirtualSat SBIR in 1998: https://sbir.nasa.gov/SBIR/abstracts/98/sbir/phase1/SBIR-98-1-13.11-5300.html
- The Hammers Company made it: https://hammers.com/virtualsat
- Not sure if we/they would be intersted in partnering?
- Could be WAAY too high fidelity. The point is to demo Major Tom, not get lost in satellite functionality...