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
