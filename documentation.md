# The NET Architecture structure explained
The output of net\_architecture\_generator.py is a json file based on a dictionary.

The dictionary contains the following:
```
net['name'] # The name of the architecture, default is "NET" + the current date and time
net['level'] # The adequate Interface Level for the architecture
net['log'] # A chronological list of UIDs and their actions in the architecture
net['online'] # A list UIDs currently online in the architecture
net['max_depth'] # The maximum depth in the architecture, used later for placing Virus
net['rooms'] # A list of dictionaries symbolising the rooms in the architecture
```
Each entry in <code>net['log']</code> list is structured as follows:
```
<UID>;<Action>;<CloakValue>
<UID>;<Action>;<CloakValue>
<UID>;<Action>;<CloakValue>
...
```

Each dictionary (room) in the <code>net['rooms']</code> list contains the following:
```
room['content'] # What the room contains (Black ICE, Password, File, Control Node)
room['owner'] # UID of the File/Control Node/Black ICE owner, None for Password
room['DV'] # The Difficulty Value of the File/Password/Control Node, empty string for Black ICE
room['depth'] # How deep the room is, used later for placing Virus
room['branch'] # A list of dictionaries symbolising the rooms in a branch
```
Limitation: The rooms in a <code>room['branch']</code> list cannot have any further branches
