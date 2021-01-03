# Design Doc

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
