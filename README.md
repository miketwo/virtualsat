# Virtual Satellite

This is a virtual satellite that you can operate! It is an extremely simple satellite model, but it can be used to practice Misson Ops.

**The goal is to download as much Value as possible**.

Value is created on the satellite via a command. Value can be downloaded with another command. Both of these actions cost Power. If you run out of power, the satellite reboots and all stored onboard Value is lost. 

Power has 2 modes: Normal and Recharging. Normal power is used when creating and downloading Value. Recharging is used to recharge. Reboots will automatically put the satellite into Recharge Mode.

There is a limited amount of onboard storage. Once it is full, the oldest entries for Value or Telemetry will be cleared to make room for newer ones.

## Getting Started

You'll want to experiment with the satellite with increasing levels of difficulty...

First things first, create a docker network for everything we'll be doing. This will allow containers to talk to each other:
```
docker network create VirtualSatNet
```

### Level 1: Flatsat

Start the satellite "on the ground" with the following command:

```
docker run --rm -it \
  -p 5001:5001/tcp \
  --name sat \
  --network VirtualSatNet \
  miketwo/virtualsat
```

*The interactive `-it` is not strictly necessary, but I find it easier to use Ctrl-C when I want to quit than `docker stop`. YMMV...*

In another terminal, start the console with the following command:

```
docker run --rm -it \
    --name console \
    --network VirtualSatNet \
    miketwo/virtualsat-console
```

This creates an interactive console with which to command the satellite (and later  groundstation).

Start by entering `satellite` to get to the satellite menu. Then type '?' to show commands.

Play with the satellite using the commands shown. **You can press enter on a blank line to get telemetry -- do this in-between other commands to see what the satellite is doing**. Try `value c` and then notice how power discharges. Try `power r` and notice how power regenerates. Try creating value until you run out of power. Try scheduling commands (using both relative and absolute times). 

You can visit http://localhost:5001/ to see current telemetry, and http://localhost:5001/history to see historical telemetry. Once you get a feel for how the satellite works, quit the satellite container and move on to the next level.

## Level 2: Orbit (under development)

Here's where things get interesting.

To launch the satellite, run the following command:

```
docker run --rm -it \
  -p 5001:5001/tcp \
  --name sat \
  --network VirtualSatNet \
  -e USE_ORBIT_PARAMETERS=TRUE \
  miketwo/virtualsat
```

Note the additional environmental parameter `USE_ORBIT_PARAMETERS`. Other env vars can be used to change the satellite name and orbit.

Now that the satellite is in orbit, **it will only respond to commands when it is over a groundstation**. You will need to deploy a groundstation. 

In a 3rd terminal, deploy a groundstation with the following:

```
docker run --rm -it \
  -p 5000:5000/tcp \
  --name gs \
  --network VirtualSatNet \
  miketwo/virtualsat-gs
```

Now you need to schedule all your commands. **Using a Mission Control will make this MUCH easier**. But for now, a few commands will be available manually. If you haven't already, start the console:

```
docker run --rm -it \
    --name console \
    --network VirtualSatNet \
    miketwo/virtualsat-console
```

You can command the groundstation to track a satellite. The console will ask you for a satellite name and the Two-Line Elements (TLEs). If you have not modified your orbital environment variables, the default satellite is:
```
STARLINK-24
1 44238U 19029D   20366.78684316  .00004289  00000-0  24662-3 0  9998
2 44238  52.9975  32.3246 0001305  89.7284 270.3857 15.14479195 87325
```
The TLEs must be copied exactly as shown. Enter the command `track`, then copy and paste the lines above in order.

The telemetry will now show the groundstation tracking the satellite, along with information about the current/next pass. Depending on when you do this, you may be in a pass or not.

===== END OF CURRENT DEMO =======

ToDo: Readme instructions for...
- Forwarding a command to the satellite during a pass
- Scheduling commands and downlinking value
- Monitoring telemetry
- Adding everything to Major Tom to show how much easier it is. 

## Level 3: Many satellites. Tbd... 

Goal: Launch 100 satellite and 10 groundstations. Manage the fleet using an awesome mission control in the cloud. Optimize operations for the most value.

## Bonus Level 4: More challenges... 

**Future work**. Many ideas here. Easy to go overboard. I'd like to do the absolute smallest change necessary to demonstrate the best features of Mission Control.
- Varying rates of charge/discharge between sats, or Sats with constraints (such as "no eclipse passes" or reduced storage)
- Non-static state (constant draining)
- Rate limits on generating/downloading value
- New axis of consideration, like thermal or GS maintanence
- Errors with mandatory diagnostic commanding. (Have to upload "diag1", "diag2", ... on different passes to get back to normal)
- Phases of flight, such as checkout. (Demonstrate scriptability)
- Performance optimizations (changing rates with "work")


# Console Reference

The console can talk to either the satellite (in flatsat mode) or a groundstation. When you first start, you must select which system to talk to.

```
Welcome! Are you talking to a satellite or groundstation?
Console> 
```

The "commands" `satellite` or `groundstation` will take you to the respective console. Quiting those will bring you back to the main console.

## Satellite Console 

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
|sched START_TIME CMD  | schedule a command at START TIME (unix time) Ex: `sched 1609459200 power r`  -- sets power to recharge at midnight on New Year's 2021 |
|rsched DELTA_SEC CMD  | for covenience, schedule commands at a RELATIVE TIME. Ex: `rsched 10 value c` -- create value in 10 seconds|


## Groundstation Console

|Tracking |                       |
|-------|--------------------------|
|track  | input tracking information for the groundstation  |

|Forward cmd (TBD) |                       |
|-------|--------------------------|
|f (any sat cmd) | immediately forward a command to the satellite  |


## ToDo's:
 - Finish Levels 2 and 3
 - Logging instead of prints
 - General code cleanup
 - Automated testing
 - Integration with MT