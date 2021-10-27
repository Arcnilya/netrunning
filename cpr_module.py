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

