import random
import sys
import os

#The purpose of this is to generate schedules for the compiler
#This works using recursion and passing a list for the filename and operations


operations = ["unroll", "interchange", "split"]
loops = ["i", "j", "q", "r"]

def generate_schedule(complexity, operation_list = [], filename_list = []):

    if complexity == 0:
        return (operation_list, filename_list)
    
    operation = random.choice(operations)
    if operation == "unroll":
        loop = random.choice(loops)
        filename_list.append(f"unroll_{loop}0")
        operation_list.append(f"unroll {loop}0")
    elif operation == "split":
        loop = random.choice(loops)
        num = random.choice([2, 4, 8, 16])
        filename_list.append(f"split_{loop}_{loop}o_{loop}i_{num}.schedule")
        operation_list.append(f"split {loop}0 {loop}0_o {loop}0_i {num}")
    else:
        loop1 = random.choice(loops)
        loop2 = random.choice(loops)
        while loop1 == loop2:
            loop2 = random.choice(loops)
        filename_list.append(f"interchange {loop1}0 {loop2}0")
        operation_list.append(f"interchange {loop1}0 {loop2}0")
    return generate_schedule(complexity -1, operation_list, filename_list)

if __name__ == "__main__":

    #Grab complexity from the user
    complexity = sys.argv[1]
    operation_list, filename_list = generate_schedule(complexity = int(complexity))
    
    #combine the filename into a string
    filename =""
    for name in filename_list:
        filename += name + "_"
    
    filename += ".schedule"
    #Write file to directory with the schedules
    if not os.path.exists("complex"):
        os.makedirs("complex")
    filename = os.path.join("complex", filename)

    with open (filename, "w") as f:
        for op in operation_list:
            f.write(op + "\n")
            print(op)
