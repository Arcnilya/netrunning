# The NET Architecture structure explained
The output of net\_architecture\_generator.py is a json file based on a dictionary.

The dictionary contains the following:
```
net['name'] # The name of the architecture, default is "NET" + the current data and time
net['level'] # The adequate Interface Level for the architecture
net['max_depth'] # The maximum depth in the architecture, used later for indicating which rooms a Virus can be planted in
net['rooms'] # A list of dictionaries symbolising the rooms in the architecture
```
Each dictionary in the <code>net['rooms']</code> list contains the following:
```
room['content'] # What the room contains (Black ICE, Password, File, Control Node)
room['depth'] # How deep the room is, used later for indicating if a Virus can be planted
room['branch'] # A list of dictionaries symbolising the rooms in a branch
```
Limitation: The rooms in a branch cannot have any further branches
