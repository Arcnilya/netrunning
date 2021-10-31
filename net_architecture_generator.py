#!/usr/bin/env python3
import random
import os
import json
import time
import argparse
import cpr_module

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
control_nodes_fname = "cpr_control_nodes"
control_nodes = []
shard_rolls = []
net_owner = "H4CK3R"


def load_control_nodes():
    lines = []
    with open(os.path.join("tables", control_nodes_fname), "r") as fp:
        lines = [l.strip() for l in fp.readlines()]
        random.shuffle(lines)
        for line in lines:
            control_nodes.append(line)


def fetch_random_shard():
    shards = os.listdir(path=r"shards")
    shard_list = [shard for shard in shards if shard.endswith(".txt")]
    random.shuffle(shard_list)
    random_shard = shard_list.pop()
    while random_shard in shard_rolls:
        random_shard = shard_list.pop()
    shard_rolls.append(random_shard)
    with open(os.path.join("shards", random_shard), "r") as fp:
        return [random_shard, fp.read()]


def load_black_ice():
    with open(os.path.join("tables", black_ice_stats_fname), "r") as fp:
        stats = fp.readlines()
        for line in stats:
            data = line.strip().split(";")
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

def get_table(fname, lvl=2):
    difficulty = max(int(lvl/2), 1)-1 # Converting from Interface level to Difficulty
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

def save_as_json(name, data): # Save in a neat json file
    with open(name+'.json', 'w') as fp:
        json.dump(data, fp, indent=4)
    print("="*37)
    print(f"Saved NET Architecture as: {name}.json")

def create_content(_content):
    content_list = []
    tmp = {}
    content = _content.split()
    if set(["Password","Control","File"]) & set(content):
        tmp['name'] = " ".join(content[:-1])
        tmp['DV'] = content[-1].replace("DV", "")
        tmp['stats'] = None
        tmp['owner'] = net_owner
        if tmp['name'] == "File":
            tmp['details'] = fetch_random_shard()
        elif tmp['name'] == "Password":
            tmp['details'] = cpr_module.password_gen(int(tmp['DV']))
        elif tmp['name'] == "Control Node":
            tmp['details'] = control_nodes.pop()
        else:
            tmp['details'] = None
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

def create_room(content, depth, branch, RID):
    return {"content":create_content(content), "depth":depth, "branch":branch, "RID":RID}

def create_branch_path(body, num_rooms, num_branches, roll_hist, curr_depth, rid):
    branch = []
    while True:
        curr_depth += 1
        roll = roll_dice(3, 6)
        while roll in roll_hist:
            roll = roll_dice(3, 6)
        roll_hist.append(roll)

        branch.append(create_room(body[roll-3], curr_depth, [], rid))
        rid += 1
        num_rooms -= 1

        # 50% chance of additional room in branch if budget allows
        room_roll = round(random.random(), 2)
        if debug: print(f"stop if {room_roll} < 0.5 or {num_rooms} <= {num_branches} * 2")
        if room_roll < 0.5 or num_rooms <= (num_branches * 2):
            break
    return branch, roll_hist

def create_main_path(net, lobby, body, num_f=None, num_b=None):
    roll_hist = []
    rooms = []
    num_rooms = roll_dice(3, 6) if num_f == None else num_f
    num_branches = roll_branch_num() if num_b == None else num_b
    num_branches = min(num_branches, int((num_rooms-2)/2)) # Limiting num_branches based on num_rooms
    if debug: print(f"floors {num_rooms}, branches {num_branches}")
    floor = 0
    rid = 0
    curr_depth = 0
    max_depth = 0
    while floor < num_rooms:
        if debug: print(f"current floor: {floor}")
        if floor < 2:   # Roll lobby table
            rooms.append(create_room(lobby.pop(), curr_depth, [], rid))
            rid += 1
        else:           # Roll body table
            roll = roll_dice(3, 6)
            while roll in roll_hist:
                roll = roll_dice(3, 6)
            roll_hist.append(roll)

            # Try to spawn branch if available
            branch = []
            branch_roll = random.random()
            if debug: print(f"branch_roll: {branch_roll} floor: {floor} num_rooms: {num_rooms} num_branches: {num_branches}")
            if debug: print(f"check branch spawn: {branch_roll} <= {floor/(num_rooms-(num_branches * 2))}")
            if num_branches > 0 and branch_roll <= floor/(num_rooms-(num_branches * 2)):
                if debug: print("Creating branch...")
                num_branches -= 1
                branch, new_roll_hist = create_branch_path(body, num_rooms-floor-1, num_branches, roll_hist, curr_depth, rid)
                if debug: print(branch)
                roll_hist = new_roll_hist
                floor += len(branch) # Update budget
                rid += len(branch) # Update RID
                max_depth = curr_depth + len(branch) if curr_depth + len(branch) > max_depth else max_depth # Update max_depth
            rooms.append(create_room(body[roll-3], curr_depth, branch, rid))
            rid += 1
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
    load_black_ice()
    load_control_nodes()

    net = {}
    net['name'] = name
    net['level'] = level
    net['log'] = [f"{net_owner};created: {net['name']};0"]
    net['online'] = []
    net['virus'] = None

    net = create_main_path(net, lobby_table, body_table, args.rooms, args.branches)

    cpr_module.print_architecture(net)
    if not args.test:
        save_as_json(name, net)

process()
