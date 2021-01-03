# Virtual Satellite

This is a virtual satellite that you can operate! 

It is an extremely simple satellite, but it can be used to practice Misson Ops.

The goal is to download as much Value as possible.

The satellite can create Value via a command. And it can download Value with another command. Both of these actions cost Power. 

Power has 2 modes: Normal and Recharging. Normal power is used when creating and downloading Value. Recharging is used to recharge. If you run out of power, the satellite reboots into a Recharge mode and all onboard Value is lost. 

Lastly, there is a limited amount of onboard storage for both Value and telemetry. Once it is full, the oldest entries will be cleared to make room for newer ones.

## Getting Started

You'll want to experiment with the satellite with increasing levels of difficulty...

### Level 1: Flatsat

Start the satellite "on the ground" with the following command:

```
docker run --rm -it \
  -p 5001:5001/tcp \
  --name sat \
  miketwo/virtualsat
```

The interactive `-it` is not strictly necessary, but I find it easier to Ctrl-C when I want to quit than use `docker stop`. YMMV...

In another terminal, start the console with the following command:

```
docker run --rm -it \
    --name console \
    --link sat \
    miketwo/virtualsat-console
```

This creates an interactive console with which to command the satellite.

Play with the satellite using the commands shown. **You can press enter on a blank line to get telemetry**. Notice how power charges/discharges. Notice how Value can be generated. Notice how if you run out of power, you lose all stored value and the reboot counter increments. Notice how telemetry is created. 

You can also visit http://localhost:5001/ to see current telemetry, and http://localhost:5001/history to see historical telemetry. Once you get a feel for how to optimally generate value, move on to the next level.

## Level 2: Orbit (under development)

Here's where things get interesting. You're putting the satellite in orbit. 

To launch the satellite, run the following command:

```
docker run --rm -it \
  -p 5001:5001/tcp \
  --name sat \
  -e USE_ORBIT_PARAMETERS=TRUE \
  miketwo/virtualsat
```

**TBD: Everything from here down is future work...**

Now that the satellite is in orbit, *it will only respond to commands when it is over a groundstation*. You will need to deploy a groundstation. 

Hopefully that can eventually be done with something like:

```
docker run --rm -it \
  -p 5000:5000/tcp \
  --name gs \
  --link sat \
  miketwo/virtualsat-gs
```

- Now you need to schedule all your commands. Using a Mission Control will make this MUCH easier.
- Add the satellite/gs/gateays to MT
- Schedule commands and downlink as much value as you can.
- Monitor telemetry to see how you're doing.

## Level 3: Many satellites. Tbd... 

Launch 100 satellites and 10 groundstations. Manage the fleet using awesome tools. Download the most value.

## Bonus Level 4: More challenges... 

Many ideas here... 


## Quickstart

In 3 terminal windows, run the following:
 - `launchsat.sh` to build and deploy a virtual satellite in a docker container
 - `launchground.sh` to build and deploy a virtual groundstation in a docker container
 - `launchconsole.sh` to build and deploy an interactive console

Commands in the console can be sent to either the satellite or groundstation.:

### Command Reference

|Power  |                   |
|-------|-------------------|
|power r|power mode recharge|
|power n|power mode normal  |

|Value |                   |
|-------|-------------------|
|value c| create value        |
|value d| downlink value    |

|Telemetry |                       |
|-------|--------------------------|
|enter  | show current telemetry   |

|Scheduling (TBD) |                       |
|-------|--------------------------|
|s START_TIME CMD  | schedule any other command at START TIME (unix time seconds)   |


#### Groundstation
- Tracking command
 - "t ????" -- track sat (TBD)
- Maintanence mode?
 - "enable gs"
 - "disable gs" - For maintanence
- Commanding
 - "f CMD" -- forward CMD to sat

Many ToDo's:
 - Finish Levels 2 and 3
 - Logging instead of prints
 - General code cleanup
 - Automated testing
