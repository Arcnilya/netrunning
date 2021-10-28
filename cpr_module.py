import os
from string import ascii_letters, punctuation, digits
from random import choice, randint, shuffle, random

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

def password_gen(DV):
    # DV6  - only shorter words
    if DV == 6 or DV == 8:
        with open(os.path.join("tables", "cpr_passwords"), "r") as fp:
            words = [w.strip() for w in fp.readlines()]
            shuffle(words)
            generated_string = words.pop()
            # DV8  - added numbers and symbols
            if DV == 8:
                generated_string = generated_string.replace("o", "0")
                generated_string = generated_string.replace("l", "1")
                generated_string = generated_string.replace("e", "3")
                if random() > 0.6:
                    generated_string += "!"

    # DV10 - passphrases
    if DV == 10:
        with open(os.path.join("tables", "common_words"), "r") as fp:
            words = [w.strip() for w in fp.readlines()]
            shuffle(words)
            generated_string = "".join(words[:3])
            if len(generated_string) < 15:
                generated_string += words[-1]
    
    # DV12 - long string of random symbols
    if DV == 12:
        string_format = ascii_letters + punctuation + digits
        generated_string = "".join(choice(string_format) for x in range(randint(15, 25)))
        generated_string.replace('"', "+") 
        generated_string.replace("'", "-") 
        generated_string.replace('\\', "/") 

    #print(f"Your DV{DV} password is:", generated_string)
    return generated_string
