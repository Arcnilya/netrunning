#!/usr/bin/env python3
import random
import os
import sys
import json
import time

debug = False
body_tables = ["cpr_net_body_table_basic","cpr_net_body_table_standard", "cpr_net_body_table_uncommon", "cpr_net_body_table_advanced"]
lobby_table_fname = "cpr_net_lobby_table"

def read_table_file(fname):
    with open(os.path.join("tables", fname), "r") as fp:
        return fp.read().strip().split(', ')

def get_body_table(lvl):
    difficulty = 3 if lvl > 8 else int(lvl/2)-1
    difficulty = 0 if difficulty < 0 else difficulty
    return read_table_file(body_tables[difficulty])

def roll_dice(x, y, z=0): # Roll xdy+z
    result = 0
    for _ in range(x):
        result += random.randint(1, y)
    return result + z

def roll_branch_num():
    branches = 0
    while random.randint(1, 10) >= 7:
        branches += 1
    return branches

def print_architecture(result):
    print(f"NET Architecture (max depth {result['max_depth']}):")
    for i,room in enumerate(result['rooms']):
        print(room['content'], f"({room['depth']})", end=' ')
        if room['branch']:
            [print('-', branch['content'], f"({branch['depth']})", end=' ') for branch in room['branch']]
        print("\n|") if i+1 < len(result['rooms']) else print("")

def save_as_json(name, result):
    with open(name+'.json', 'w') as fp:
        json.dump(result, fp, indent=4)

def create_branch_path(body, num_floors, num_branches, roll_hist, curr_depth):
    branch = []
    while True:
        curr_depth += 1
        roll = roll_dice(3, 6)
        while roll in roll_hist:
            roll = roll_dice(3, 6)
        roll_hist.append(roll)
        room = {"content":body[roll-3], "depth":curr_depth, "branch":[]} # Branches cannot have new branches
        branch.append(room) 
        num_floors -= 1

        # 50% chance of additional room in branch if budget allows
        room_roll = round(random.random(), 2)
        if debug: print(f"stop if {room_roll} < 0.5 or {num_floors} <= {num_branches} * 2")
        if room_roll < 0.5 or num_floors <= (num_branches * 2):
            break
    return branch, roll_hist

def create_main_path(lobby, body, num_f=None, num_b=None):
    net_architecture = {}
    roll_hist = []
    rooms = []
    num_floors = roll_dice(3, 6) if num_f == None else num_f
    num_branches = roll_branch_num() if num_b == None else num_b
    if debug: print(f"floors {num_floors}, branches {num_branches}")
    floor = 0
    curr_depth = 0
    max_depth = 0
    while floor < num_floors:
        if debug: print(f"current floor: {floor}")
        if floor < 2:   # Roll lobby table
            room = {"content":lobby.pop(), "depth":curr_depth, "branch":[]}
            rooms.append(room)
        else:           # Roll body table
            roll = roll_dice(3, 6)
            while roll in roll_hist:
                roll = roll_dice(3, 6)
            roll_hist.append(roll)

            # Try to spawn branch if available
            branch = []
            branch_roll = random.random()
            if debug: print(f"branch_roll: {branch_roll} floor: {floor} num_floors: {num_floors} num_branches: {num_branches}")
            if debug: print(f"check branch spawn: {branch_roll} <= {floor/(num_floors-(num_branches * 2))}")
            if num_branches > 0 and branch_roll <= floor/(num_floors-(num_branches * 2)):
                if debug: print("Creating branch...")
                num_branches -= 1
                branch, new_roll_hist = create_branch_path(body, num_floors-floor-1, num_branches, roll_hist, curr_depth)
                if debug: print(branch)
                roll_hist = new_roll_hist
                floor += len(branch) # Update budget
                max_depth = curr_depth + len(branch) if curr_depth + len(branch) > max_depth else max_depth # Update max_depth
            room = {"content":body_table[roll-3], "depth":curr_depth, "branch":branch}
            rooms.append(room)
        max_depth = curr_depth if curr_depth > max_depth else max_depth
        curr_depth += 1
        floor += 1
    net_architecture['max_depth'] = max_depth
    net_architecture['rooms'] = rooms
    return net_architecture


name = input("Architecture Name: ")
name = "NET-"+time.strftime("%Y%m%d-%H%M%S") if name == "" else name
level = input("Interface Level: ")
level = 2 if level == "" else int(level)
lobby_table = read_table_file(lobby_table_fname)
random.shuffle(lobby_table)
body_table = get_body_table(level)

if len(sys.argv) == 3:
    net = create_main_path(lobby_table, body_table, int(sys.argv[1]), int(sys.argv[2]))
else:
    net = create_main_path(lobby_table, body_table)

print_architecture(net)
save_as_json(name, net)

