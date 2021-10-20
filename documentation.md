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
Each dictionary (room) in the <code>net['rooms']</code> list contains the following:
```
room['content'] # What the room contains (Black ICE, Password, File, Control Node)
room['depth'] # How deep the room is, used later for placing Virus
room['branch'] # A list of dictionaries symbolising the rooms in a branch
```
Limitation: The rooms in a <code>room['branch']</code> list cannot have any further branches
