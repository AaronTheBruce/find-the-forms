def promptAction(prompt):
    while prompt == True:
        print("Search by Form Name(s): Press F")
        print("Download Forms by earliest to latest year: Press D")
        action = input("What Action do you want to take?: ")
        if action == 'F' or action == 'f':
            prompt = False
            return 'F'
        elif action == 'D' or action == 'd':
          prompt = False
          return 'D'  
        else:
            print("Invalid Input")