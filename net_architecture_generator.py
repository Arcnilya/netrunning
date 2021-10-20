#!/usr/bin/env python3
import random
import os
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", type=str, default="", help="name of the net architecture")
parser.add_argument("-l", "--level", type=int, default=2, help="netrunner interface level")
parser.add_argument("-r", "--rooms", type=int, default=None, help="number of rooms")
parser.add_argument("-b", "--branches", type=int, default=None, help="number of branches")
parser.add_argument("-t", "--test", action="store_true", help="skips saving as json")
parser.add_argument("-d", "--debug", action="store_true", help="run as verbose with debug info")
args = parser.parse_args()


debug = True if args.debug else False
body_matrix_fname = "cpr_net_body_matrix"
lobby_table_fname = "cpr_net_lobby_table"

def get_table(fname, lvl=0):
    difficulty = 3 if lvl > 8 else int(lvl/2)-1 # Converting from Interface level to Difficulty
    difficulty = 0 if difficulty < 0 else difficulty # Safe input for negative values
    with open(os.path.join("tables", fname), "r") as fp:
        return fp.readlines()[difficulty].strip().split(', ')

def roll_dice(x, y, z=0): # Roll xdy+z
    result = 0
    for _ in range(x):
        result += random.randint(1, y)
    return result + z

def roll_branch_num(): # Roll for the number of branches in the architecture
    branches = 0
    while random.randint(1, 10) >= 7:
        branches += 1
    return branches

def print_architecture(result): # Nice output in the console
    print("="*37)
    print(f"NET Architecture: {result['name']}")
    print(f"Level: {result['level']} Max Depth: {result['max_depth']}")
    for i,room in enumerate(result['rooms']):
        print(room['content'], f"({room['depth']})", end=' ')
        if room['branch']:
            [print('-', branch['content'], f"({branch['depth']})", end=' ') for branch in room['branch']]
        print("\n|") if i+1 < len(result['rooms']) else print("")

def save_as_json(name, data): # Save in a neat json file
    with open(name+'.json', 'w') as fp:
        json.dump(data, fp, indent=4)
    print("="*37)
    print(f"Saved NET Architecture as: {name}.json")

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

def create_main_path(net, lobby, body, num_f=None, num_b=None):
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
    net['max_depth'] = max_depth
    net['rooms'] = rooms
    return net


#name = input("Architecture Name (optional): ")
name = "NET-"+time.strftime("%Y%m%d-%H%M%S") if args.name == "" else args.name
#level = input("Interface Level [2]: ")
# https://gist.github.com/baybatu/269296fe1d530f0defff7b6454222bc0
level = max(min(args.level, 8), 0) # Default 2
lobby_table = get_table(lobby_table_fname)
random.shuffle(lobby_table)
body_table = get_table(body_matrix_fname, level)

net = {}
net['name'] = name
net['level'] = level

net = create_main_path(net, lobby_table, body_table, args.rooms, args.branches)

print_architecture(net)
if not args.test:
    save_as_json(name, net)

