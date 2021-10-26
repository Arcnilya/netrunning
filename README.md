# netrunning
Netrunning scripts for Cyberpunk Red

## net\_architecture\_generator (Work in Progress)
Generates a balanced NET Architecture for Netrunning in Cyberpunk Red based on the Interface level of a Netrunner.

[NET Arcnitecture structure explained](documentation.md)

### Usage (WIP)
```
python3 net_architecture_generator.py -r 10 -b 2 -l 2
=====================================
NET Architecture: NET-20211026-102210
Level: 2 Max Depth: 7
Skunk (0) 
|
Password DV6 (1) 
|
File DV6 (2) 
|
Wisp (3) - Raven (4) 
|
Raven + Raven (4) 
|
Password DV6 (5) - Skunk (6) - Control Node DV6 (7) 
|
Password DV6 (6) 
=====================================
Saved NET Architecture as: NET-20211026-102210.json
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
9. Create a default log
10. Add text to Files, passwords to Passwords, nodes to Control Nodes
11. Add Virus instructions to the NET Architecture
12. Add "logged-in Netrunners" (UIDs) and their HP

## net\_architecture\_runner (Coming Soon)
Simulates Netrunning in Cyberpunk Red with a Command Line Interface using NET Architectures (from e.g., the net\_architecture\_generator).

### Features
- Two options for password: enter correct (3 tries) or bruteforce (roll against DV)
- Log all actions in the Architecture and print the log when succeeding the Pathfinder DV. Use a handle (or a random number) to track actions and associate DVS.
- Track the Program's REZ and any Netrunner's brain damage.   
