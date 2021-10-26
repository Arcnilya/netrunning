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
black_ice_stats_fname = "cpr_black_ice_stats"
black_ice_stats = {}
net_owner = "H4CK3R"

def load_black_ice(fname):
    with open(os.path.join("tables", fname), "r") as fp:
        stats = fp.readlines()
        for line in stats:
            data = line.strip().split(";")
            #print(data[0])
            stats = {}
            stats["class"] = data[1]
            stats["PER"] = data[2]
            stats["SPD"] = data[3]
            stats["ATK"] = data[4]
            stats["DEF"] = data[5]
            stats["REZ"] = data[6]
            stats["effect"] = data[7]
            stats["cost"] = data[8]
            black_ice_stats[data[0]] = stats
    #print(json.dumps(black_ice_stats, indent=4))


def get_table(fname, lvl=0):
    difficulty = int(lvl/2)-1 # Converting from Interface level to Difficulty
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

def print_room(room):
    for i, content in enumerate(room['content']):
        DV = "" if not content['DV'] else f"DV{content['DV']} "
        print(f"{content['name']} {DV}", end='')
        if i < len(room['content'])-1:
            print("+", end=' ')
    print(f"({room['depth']})", end=' ')

def print_architecture(result): # Nice output in the console
    print("="*37)
    print(f"NET Architecture: {result['name']}")
    print(f"Level: {result['level']} Max Depth: {result['max_depth']}")
    for i,main_room in enumerate(result['rooms']):
        print_room(main_room)
        if main_room['branch']:
            for branch_room in main_room['branch']:
                print("- ", end="")
                print_room(branch_room)
        print("\n|") if i+1 < len(result['rooms']) else print("")

def save_as_json(name, data): # Save in a neat json file
    with open(name+'.json', 'w') as fp:
        json.dump(data, fp, indent=4)
    print("="*37)
    print(f"Saved NET Architecture as: {name}.json")

def create_content(content):
    content_list = []
    tmp = {}
    content = content.split()
    if set(["Password","Control","File"]) & set(content):
        tmp['name'] = " ".join(content[:-1])
        tmp['DV'] = content[-1][2:]
        tmp['stats'] = None
        tmp['owner'] = net_owner
        tmp['details'] = "foo" if tmp['name'] == "File" else None
        content_list.append(tmp)
    else: # Black ICE
        for ice_name in content:
            tmp = {}
            tmp['name'] = ice_name
            tmp['DV'] = None
            tmp['stats'] = black_ice_stats[ice_name]
            tmp['owner'] = net_owner
            tmp['details'] = None
            content_list.append(tmp)
    return content_list

def create_room(content, depth, branch):
    return {"content":create_content(content), "depth":depth, "branch":branch}

def create_branch_path(body, num_floors, num_branches, roll_hist, curr_depth):
    branch = []
    while True:
        curr_depth += 1
        roll = roll_dice(3, 6)
        while roll in roll_hist:
            roll = roll_dice(3, 6)
        roll_hist.append(roll)

        branch.append(create_room(body[roll-3], curr_depth, [])) 
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
            rooms.append(create_room(lobby.pop(), curr_depth, []))
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
            rooms.append(create_room(body[roll-3], curr_depth, branch))
        max_depth = curr_depth if curr_depth > max_depth else max_depth
        curr_depth += 1
        floor += 1
    net['max_depth'] = max_depth
    net['rooms'] = rooms
    return net


def process():
    name = "NET-"+time.strftime("%Y%m%d-%H%M%S") if args.name == "" else args.name
    # https://gist.github.com/baybatu/269296fe1d530f0defff7b6454222bc0
    level = max(min(args.level, 8), 0) # Default 2
    lobby_table = get_table(lobby_table_fname)
    random.shuffle(lobby_table)
    body_table = get_table(body_matrix_fname, level)
    load_black_ice(black_ice_stats_fname)

    net = {}
    net['name'] = name
    net['level'] = level
    net['log'] = []
    net['online'] = []

    net = create_main_path(net, lobby_table, body_table, args.rooms, args.branches)

    print_architecture(net)
    if not args.test:
        save_as_json(name, net)

process()
