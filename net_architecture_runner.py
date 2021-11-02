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

class runner():
    def __init__(self, _net):
        self.net = _net
        self.curr_UID = ""
        self.curr_cloak = 0
        self.curr_room = 0

    def menu(self):
        self.login()
        self.check_virus()
        self.print_menu()
        choice = int(input("> "))
        while choice != 0:
            if choice == 1:
                self.cloak()
            elif choice == 2:
                self.pathfinder()
            else:
                break
            self.print_menu()
            choice = int(input("> "))

        self.logout()
        self.save_net()    

    def pathfinder(self):
        # Two parts: reveal log and reveal rooms
        pf_value = int(input("Enter rolled PathfinderValue: "))
        print("Log:")
        print("=" * 37)
        for action in self.net['log']:
            if action[0] == self.curr_UID:
                # You ALWAYS see your own activity
                print(f"{action[0]}: {action[1]} (you)") 
            elif action[2] < pf_value:
                print(f"{action[0]}: {action[1]}")
        print("=" * 37, "\n")
        # TODO reveal rooms

    def cloak(self):
        cloak_value = int(input("Enter rolled CloakValue: "))
        self.curr_cloak = cloak_value  # Update cloak 
        for action in self.net['log']: # Update log
            if action[0] == self.curr_UID:
                action[2] = self.curr_cloak
        print("Cloak successfully applied.")

    def print_menu(self):
        print("=" * 10)
        print("0: exit")
        print("1: cloak")
        print("2: pathfinder")
        print("=" * 10)

    def check_virus(self):
        if self.net['virus']:
            print(f"VIRUS! {self.net['virus']}")

    def clear_log(self):
        self.net['log'] = self.net['log'][:1]

    def log_action(self, action):
        self.net['log'].append([self.curr_UID, action, self.curr_cloak])

    def save_net(self):
        if clear:
            self.clear_log()
        with open(self.net['name']+'.json', 'w') as fp:
            json.dump(self.net, fp, indent=4)
    
    def is_UID_online(self, UID):
        if any(UID == user[0] for user in self.net['online']):
            return True
        else:
            return False

    def login(self):
        while True:
            uname = input("Enter UID (Leave empty for random): ")
            if uname == "": # Generate random UID
                uname = cpr_module.get_random_UID()
                while self.is_UID_online(uname):
                    uname = cpr_module.get_random_UID()
            if self.is_UID_online(uname):
                print("UID already logged in, try again.")
            else:
                break
        hp = 69
        self.curr_UID = uname
        self.net['online'].append([self.curr_UID, hp, self.curr_room])
        self.log_action("Logged in")
        print(f"You are now logged in as: {self.curr_UID}")

    def logout(self):
        for user in self.net['online']:
            if self.curr_UID == user[0]:
                self.net['online'].remove(user)
                break
        self.log_action("Logged out")
        print(f"You have now logged out as: {self.curr_UID}")

def load_net(fname):
    with open(fname, "r") as fp:
        return json.load(fp)

def main():
    if args.net.endswith(".json"):
        net = load_net(args.net)    
        print("Loaded the NET from the json file.")
    else:
        print("-n/--net must be a json file.")
        exit(0)

    r = runner(net)
    r.menu()




if __name__ == '__main__':
    main()
