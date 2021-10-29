# netrunning
Netrunning scripts for Cyberpunk Red

## net\_architecture\_generator (Work in Progress)
Generates a balanced NET Architecture for Netrunning in Cyberpunk Red based on the Interface level of a Netrunner.

[NET Arcnitecture structure explained](documentation.md)

### Usage (WIP)
```
python3 net_architecture_generator.py --rooms 8 --branches 1 --level 4
=====================================
NET Architecture: NET-20211028-141420
Level: 4 Max Depth: 5
File DV6 (0) 
|
Skunk (1) 
|
Sabertooth (2) - Hellhound (3) - Scorpion (4) 
|
File DV8 (3) 
|
Password DV8 (4) 
|
Control Node DV8 (5) 
=====================================
Saved NET Architecture as: NET-20211028-141420.json
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
10. Create lists of passwords, file content and control nodes
    - ~~Have different passwords for different DVs (matching entropy)~~
    - Get file content from CP2077 shards, linux kernel, CS poetry
11. Add Virus instructions to the NET Architecture
12. Add "logged-in Netrunners" (UIDs) and their HP

## net\_architecture\_runner (Coming Soon)
Simulates Netrunning in Cyberpunk Red with a Command Line Interface using NET Architectures (from e.g., the net\_architecture\_generator).

### Features
- Two options for password: enter correct (3 tries) or bruteforce (roll against DV)
- Log all actions in the Architecture and print the log when succeeding the Pathfinder DV. Use a handle (or a random number) to track actions and associate DVS.
- Track the Program's REZ and any Netrunner's brain damage.   
