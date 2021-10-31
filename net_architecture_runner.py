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
args = parser.parse_args()


debug = True if args.debug else False
curr_UID = ""
curr_cloak = 0

def load_net(fname):
    with open(fname, "r") as fp:
        return json.load(fp)

def save_net(net):
    with open(net['name']+'.json', 'w') as fp:
        json.dump(net, fp, indent=4)

def login(net):
    while True:
        uname = input("Enter UID (Leave empty for random): ")
        uname = uname if not uname == "" else cpr_module.get_random_UID()
        if any(uname == o.split(';')[0] for o in net['online']):
            print("UID already logged in, try again.")
        else:
            break
    hp = 69
    global curr_UID
    curr_UID = uname
    net['online'].append(f"{curr_UID};{hp};{0}")
    net['log'].append(f"{curr_UID};Logged in;{curr_cloak}")
    print(f"You are now logged in as: {curr_UID}")
    return net

def logout(net):
    for o in net['online']:
        if curr_UID == o.split(';')[0]:
            net['online'].remove(o)
            break
    net['log'].append(f"{curr_UID};Logged out;{curr_cloak}")
    return net

def process():
    if args.net.endswith(".json"):
        net = load_net(args.net)    
    else:
        print("-n/--net must be a json file.")
        exit(0)
    print("Loaded the NET from the json file.")
    net = login(net)
    #print(json.dumps(net, indent=4))

    net = logout(net)
    save_net(net)    

process()
