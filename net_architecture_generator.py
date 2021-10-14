#!/usr/bin/env python3
import random
import os

body_tables = ["cpr_net_body_table_basic","cpr_net_body_table_standard", "cpr_net_body_table_uncommon", "cpr_net_body_table_advanced"]
lobby_table_fname = "cpr_net_lobby_table"

def read_table_file(fname):
    fp = open(os.path.join("tables", fname), "r")
    table = fp.read().strip().split(', ')
    fp.close()
    return table

def get_body_table(lvl):
    difficulty = 3 if lvl > 8 else int(lvl/2)-1
    difficulty = 0 if difficulty < 0 else difficulty
    return read_table_file(body_tables[difficulty])

def roll_dice(x, y, z=0): # Roll 3d6 for the total number of floors
    result = 0
    for _ in range(x):
        result += random.randint(1, y)
    return result + z

def roll_branch_num():
    branches = 0
    while True:
        if random.randint(1, 10) >= 7:
            branches += 1
        else:
            break
    return branches


level = int(input("Interface Level: "))
lobby_table = read_table_file(lobby_table_fname)
random.shuffle(lobby_table)
body_table = get_body_table(level)

num_floors = roll_dice(3, 6)
num_branches = roll_branch_num() # Todo
#print(num_floors, num_branches)

roll_hist = []
architecture = []
for floor in range(num_floors):
    if floor < 2: # Roll lobby table
        architecture.append(lobby_table.pop())
    else: # Roll body table
        roll = roll_dice(3, 6)
        while roll in roll_hist:
            roll = roll_dice(3, 6)
        architecture.append(body_table[roll-3])
        roll_hist.append(roll)
print(architecture)



