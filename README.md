# netrunning
Netrunning scripts for Cyberpunk Red

## net\_architecture\_generator (Work in Progress)
Generates a balanced NET Architecture for Netrunning in Cyberpunk Red based on the Interface level of a Netrunner.

### Usage (WIP)
```
python3 net_architecture_generator.py
Architecture Name (optional): 
Interface Level [2]: 
=====================================
NET Architecture: NET-20211019-142110
Level: 2 Max Depth: 6
Wisp (0) 
|
Skunk (1) 
|
Raven x2 (2) 
|
Password DV6 (3) - Control Node DV6 (4) 
|
Asp (4) 
|
Killer + Skunk (5) 
|
File DV6 (6) 
```

### Todo
1. ~~Change structure to a list of dictionaries instead of a list of lists~~
2. ~~Save NET Architecture to JSON~~
3. ~~Add max\_depth to the NET Architecture~~
4. ~~Merge roll-tables to one single file~~
5. Add a log to the NET Architecture with UIDs
6. Add Black ICE stats (Name, Class, PER, SPD, ATK, DEF, REZ, Effect)
7. Add owner to Control Nodes (UIDs)
8. Add content to Files (flavor text)
9. Add Virus instructions to the NET Architecture
10. Add "logged-in Netrunners" (UIDs) and their HP

## net\_architecture\_runner (Coming Soon)
Simulates Netrunning in Cyberpunk Red with a Command Line Interface using NET Architectures (from e.g., the net\_architecture\_generator).

### Features
- Two options for password: enter correct (3 tries) or bruteforce (roll against DV)
- Log all actions in the Architecture and print the log when succeeding the Pathfinder DV. Use a handle (or a random number) to track actions and associate DVS.
- Track the Program's REZ and any Netrunner's brain damage.   
