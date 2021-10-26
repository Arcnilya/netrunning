# The NET Architecture structure explained
The output of net\_architecture\_generator.py is a json file based on a dictionary.

The dictionary contains the following:
```
net['name']         # The name of the architecture, default is "NET" + the current date and time
net['level']        # The adequate Interface Level for the architecture
net['log']          # A chronological list of UIDs and their actions in the architecture
net['online']       # A list UIDs currently online in the architecture
net['max_depth']    # The maximum depth in the architecture, used later for placing Virus
net['rooms']        # A list of dictionaries representing the rooms in the architecture
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
room['content']     # What the room contains (see below)
room['depth']       # How deep the room is, used later for placing Virus
room['branch']      # A list of dictionaries symbolising the rooms in a branch
```
Note: The rooms in a <code>room['branch']</code> list do not have any further branches

Each content in <code>room['content']</code> contains the following:
```
content['name']     # Name of the content
content['DV']       # Difficulty Value of the File or Password or Control Node (empty string for Black ICE)
content['stats']    # Stats for Black ICE (None for other content)
content['owner']    # UID of the File or Control Node or Black ICE owner (None for Password
content['details']  # File text, Password password, Control Node node, None for Black ICE
```

Each stats in <code>content['stats']</code> contains the following:
```
stats['class']      # Anti-Personnel or Anti-Program
stats['PER']        # Perception 
stats['SPD']        # Speed
stats['ATK']        # Attack
stats['DEF']        # Defense
stats['REZ']        # Health
stats['effect']     # Effect
stats['cost']       # Price in eb
```
