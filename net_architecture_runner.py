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

def load_net(fname):
    with open(fname, "r") as fp:
        return json.load(fp)


def process():
    if args.net.endswith(".json"):
        net = load_net(args.net)    
    else:
        print("-n/--net must be a json file.")
        exit(0)
    #print(json.dumps(net, indent=4))
    print("Loaded the NET from the json file.")
    

process()
