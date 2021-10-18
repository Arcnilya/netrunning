# netrunning
Netrunning scripts for Cyberpunk Red

## net\_architecture\_generator (Work in Progress)
Generates a balanced NET Architecture for Netrunning in Cyberpunk Red based on the Interface level of a Netrunner.

### Usage (WIP)
```
python3 net_architecture_generator.py
Interface Level: 2
Max depth: 7
NET Architecture:
Skunk (0) 
|
Password DV8 (1) 
|
Control Node DV6 (2) 
|
Skunk (3) 
|
Scorpion (4) - Password DV6 (5) - File DV6 (6) 
|
Raven (5) 
|
Password DV6 (6) 
|
Wisp (7) 
```

### Todo
1. Change structure to a list of dictionaries instead of a list of lists
2. Save NET Architecture to JSON
3. Add a log to the NET Architecture with UIDs
4. Add Black ICE stats (Name, Class, PER, SPD, ATK, DEF, REZ, Effect)
5. Add owner to Control Nodes (UIDs)
6. Add content to Files (flavor text)
7. Add Virus instructions to the NET Architecture
8. Add "logged-in Netrunners" (UIDs) and their HP

## net\_architecture\_runner (Coming Soon)
Simulates Netrunning in Cyberpunk Red with a Command Line Interface using NET Architectures (from e.g., the net\_architecture\_generator).

### Features
- Two options for password: enter correct (3 tries) or bruteforce (roll against DV)
- Log all actions in the Architecture and print the log when succeeding the Pathfinder DV. Use a handle (or a random number) to track actions and associate DVS.
- Track the Program's REZ and any Netrunner's brain damage.   
