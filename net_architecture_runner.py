#!/usr/bin/env python3
import random
import os
import json
import time
import argparse
import cpr_module


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--net", type=str, required=True, help="name of the net architecture")
parser.add_argument("-d", "--debug", action="store_true", help="run as verbose with debug info")
parser.add_argument("-c", "--clear", action="store_true", help="clear the log before exiting")
args = parser.parse_args()


debug = True if args.debug else False
clear = True if args.clear else False
curr_UID = ""
curr_cloak = 0
curr_room = 0

def clear_log(net):
    first_entry = net['log'][0]
    net['log'].clear()
    net['log'].append(first_entry)
    return net

def log_action(net, action):
    net['log'].append([curr_UID, action, curr_cloak])
    return net

def load_net(fname):
    with open(fname, "r") as fp:
        return json.load(fp)

def save_net(net):
    net = clear_log(net) if clear else net
    with open(net['name']+'.json', 'w') as fp:
        json.dump(net, fp, indent=4)

def login(net):
    while True:
        uname = input("Enter UID (Leave empty for random): ")
        uname = uname if not uname == "" else cpr_module.get_random_UID()
        if any(uname == user[0] for user in net['online']):
            print("UID already logged in, try again.")
        else:
            break
    hp = 69
    global curr_UID
    curr_UID = uname
    net['online'].append([curr_UID, hp, curr_room])
    net = log_action(net, "Logged in")
    print(f"You are now logged in as: {curr_UID}")
    return net

def logout(net):
    for user in net['online']:
        if curr_UID == user[0]:
            net['online'].remove(user)
            break
    net = log_action(net, "Logged out")
    print(f"You have now logged out as: {curr_UID}")
    return net

def process():
    if args.net.endswith(".json"):
        net = load_net(args.net)    
        print("Loaded the NET from the json file.")
    else:
        print("-n/--net must be a json file.")
        exit(0)
    net = login(net)
    #print(json.dumps(net, indent=4))
    tmp = input("Press enter to exit:")
    net = logout(net)
    save_net(net)    

process()
