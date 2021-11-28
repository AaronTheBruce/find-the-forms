def promptAction(prompt):
    while prompt == True:
        print("Search by Form Name(s): Press F")
        action = input("What Action do you want to take?: ")
        if action == 'F' or action == 'f':
            prompt = False
            return 'F'
        else:
            print("Invalid Input")