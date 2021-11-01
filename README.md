# netrunning
Netrunning scripts for Cyberpunk Red

## net\_architecture\_generator (Draft 1.0)
Generates a balanced NET Architecture for Netrunning in Cyberpunk Red based on the Interface level of a Netrunner.

[NET Arcnitecture structure explained](documentation.md)

### Usage (Output subject to change)
```
python3 net_architecture_generator.py --rooms 5 --branches 0 --level 2
=====================================
NET Architecture: NET-20211101-120226
Level: 2 Max Depth: 4
Password DV6 (0) 
|
Killer (1) 
|
Wisp (2) 
|
File DV6 (3) 
|
Raven (4) 
=====================================
Saved NET Architecture as: NET-20211101-120226.json
```

### Todo
1. ~~Change structure to a list of dictionaries instead of a list of lists~~
2. ~~Save NET Architecture to JSON~~
3. ~~Add max\_depth to the NET Architecture~~
4. ~~Merge roll-tables to one single file~~
5. ~~Add Architecture Name and Interface Level to argparse~~
6. ~~Add a log to the NET Architecture with UIDs~~
7. ~~Restructure content in rooms~~ [link](documentation.md)
8. ~~Add Black ICE stats (Name, Class, PER, SPD, ATK, DEF, REZ, Effect, cost)~~
9. ~~Create a default log~~
10. ~~Create lists of passwords, file content and control nodes~~
    - ~~Have different passwords for different DVs (matching entropy)~~
    - ~~Get file content from CP2077 shards, linux kernel, CS poetry~~
11. ~~Add Virus instructions to the NET Architecture~~
12. ~~Add "logged-in Netrunners" (UIDs) and their HP~~

## net\_architecture\_runner (Work In Progress)
Simulates Netrunning in Cyberpunk Red with a Command Line Interface using NET Architectures (from e.g., the net\_architecture\_generator).

### Usage (WIP)
```
python3 net_architecture_runner.py --net NET-20211031-005605.json
Loaded the NET from the json file.
```

### Todo
1. ~~Change net['online'] and net['log'] to nested lists~~
2. Change to classes instead
3. Print Virus on login
4. Add Pathfinder

### Ideas / Brainstorm
- Should Netrunners be able to load their Cyberdecks?
- How often should any changes be saved to disk?
- Print out Virus instructions (if any) when entering
- Need a way to track where the Netrunner is, add room IDs and track in Online list?
- Two options for password: enter correct (3 tries) or bruteforce (roll against DV)
- Log all actions in the Architecture and print the log when succeeding the Pathfinder DV. Use a handle (or a random number) to track actions and associate DVS.
- Track the Program's REZ and any Netrunner's brain damage.

## net\_architecture\_forger (Coming Soon)
Similar to generator, but less automation and more manual control.
