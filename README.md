# Virtual Satellite




- Launch the satellite and go to localhost:5001/ to see the satellite status
- Launch the groundstation and go to localhost:5000/ to see the status
- Launch the console and use it to command both

Level 1: Flatsat
- Play with the satellite using the commands and buttons on debug. (Or MT interactive mode). Notice how power charges/discharges. Notice how value can be generated. Notice how if you run out of power, you lose all stored value. Notice how telemetry is created. Downlink as much value as you can.

Level 2: Orbit
- Now you need to schedule all your commands using MT. Add the satellite to MT
- Add a Groundstation (need to dockerize this as well)
- Add a Gateway (?)
- Schedule commands and downlink as much value as you can.

Level 3: Tbd... (more realism? manage thermal + other subsystems)


## Quickstart

In 3 terminal windows, run the following:
 - `launchsat.sh` to build and deploy a virtual satellite in a docker container
 - `launchground.sh` to build and deploy a virtual groundstation in a docker container
 - `launchconsole.sh` to build and deploy an interactive console

Commands in the console can be sent to either the satellite or groundstation.:

### Commands

|Basic   |                   |
|--------|-------------------|
|ping gs |ping the groundstation|
|ping sat|ping the satellite  |

#### Satellite

|Power  |                   |
|-------|-------------------|
|power r|power mode recharge|
|power n|power mode normal  |

|Value |                   |
|-------|-------------------|
|value t| create value        |
|value d| downlink value    |

|Telemetry |                       |
|-------|--------------------------|
|tlm d  | show current telemetry   |
|tlm h  | download all tlm history |


|Scheduling |                       |
|-------|--------------------------|
|s START_TIME CMD  | schedule any other command at START TIME (unix time seconds)   |


#### Groundstation
- Tracking
 - "t ????" -- track sat (TBD)
- Maintanence
 - "enable gs"
 - "disable gs" - For maintanence
- Commanding
 - "f CMD" -- forward CMD to sat

ToDo:
 - API interface
 - Logging instead of prints
 - Make docker work. Publish to registry.
 - Interactive flatsat mode that ignores GS location?


## Design Principles

### STAY SIMPLE:
 - Operator must balance Creating Value, Downlinking, and Recharging.

 - We must correctly simulate communication over a groundstation. The groundstation's lat/long can be included with each API call. That is used to determine if comms is possible.

 - We must communicate with the satellite over a json API, not programmatically. The satellite code should be a black box.

 - The groundstation must be extremely simple. Just adds its own location to the commands.

 - It would be nice if they were each containers that talked to each other. It would also be nice if the GS and Satellite have no idea what Major Tom is, to better simulate interfacing with 3rd party systems.

 - We need to connect to Major Tom (Gateway to GS?)


## Program properties
The satellite keeps track of the following state:
  - Onboard Storage, including
    - Telemetry history
    - Value history
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
   - It costs extra power to create value
   - It costs extra power to download value
   - Reaching 0 power causes a reboot. Sat automatically switches to "recharge mode"
 - It takes XX orbits to recharge fully.

### Communication Subsystem
  - Upload commands (scheduled or immediate)
  - Downlink value
  - Downlink telemetry
    - All TLM can be downloaded instantaneously

### Scheduling Subsystem
  - Schedule a command (time, command)
  - Cancel a scheduled command

### Value Subsystem
  - Creates value
  - Value is created on demand
    -- It costs power to create value
    -- There is a maximum amount that can be stored. Asking for more drops old value.


## Other notes

3rd Party?
- There was a VirtualSat SBIR in 1998: https://sbir.nasa.gov/SBIR/abstracts/98/sbir/phase1/SBIR-98-1-13.11-5300.html
- The Hammers Company made it: https://hammers.com/virtualsat
- Not sure if we/they would be intersted in partnering?
- Could be WAAY too high fidelity. The point is to demo Major Tom, not get lost in satellite functionality...
