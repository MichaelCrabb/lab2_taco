import random
import sys
import os

#The purpose of this is to generate schedules for the compiler
#This works using recursion and passing a list for the filename and operations

"""
Example Usage:
    python generate.py <num_schedules> <complexity>
    python generate.py 5 3  # Generates 5 different schedules, each with 3 operations
"""

operations = ["unroll", "interchange", "split"]
loops = ["i", "j", "q", "r"]

def generate_schedule(complexity):
    """
    Recursively generates a single schedule of loop transformations.
    
    Args:
        complexity (int): Number of operations to generate
    
    Returns:
        tuple: (operation_list, filename_list) containing the generated
               operations and their filename representations
    """
    def _generate_recursive(remaining_complexity, operation_list, filename_list):
        if remaining_complexity == 0:
            return operation_list, filename_list
        
        # Randomly select a transformation operation
        operation = random.choice(operations)
        
        if operation == "unroll":
            # Unroll operation: Unrolls a selected loop
            loop = random.choice(loops)
            filename_list.append(f"unroll_{loop}0")
            operation_list.append(f"unroll {loop}0")
            
        elif operation == "split":
            # Split operation: Splits a loop with a given factor
            loop = random.choice(loops)
            # Common split factors used in loop optimization
            num = random.choice([2, 4, 8, 16])
            filename_list.append(f"split_{loop}_{loop}o_{loop}i_{num}.schedule")
            operation_list.append(f"split {loop}0 {loop}0_o {loop}0_i {num}")
            
        else:  # interchange operation
            # Interchange operation: Swaps two different loops
            loop1 = random.choice(loops)
            loop2 = random.choice(loops)
            # Ensure we select two different loops
            while loop1 == loop2:
                loop2 = random.choice(loops)
            filename_list.append(f"interchange {loop1}0 {loop2}0")
            operation_list.append(f"interchange {loop1}0 {loop2}0")
            
        return _generate_recursive(remaining_complexity - 1, operation_list, filename_list)
    
    # Start with fresh lists for each schedule
    return _generate_recursive(complexity, [], [])

def generate_multiple_schedules(num_schedules, complexity):
    """
    Generates multiple different schedules with the specified complexity.
    
    Args:
        num_schedules (int): Number of different schedules to generate
        complexity (int): Number of operations in each schedule
    
    Returns:
        None: Writes schedules directly to files
    """
    # Create output directory if it doesn't exist
    if not os.path.exists("complex"):
        os.makedirs("complex")
        
    for i in range(num_schedules):
        # Generate a fresh schedule each time
        operation_list, filename_list = generate_schedule(complexity)
        
        # Construct filename from the list of operations
        filename = f"schedule_{i+1}_"  # Add schedule number to filename
        for name in filename_list:
            filename += name + "_"
        
        filename += ".schedule"
        filepath = os.path.join("complex", filename)
        
        # Write operations to the schedule file
        with open(filepath, "w") as f:
            print(f"\nGenerating Schedule {i+1}:")
            for op in operation_list:
                f.write(op + "\n")
                print(op)

if __name__ == "__main__":
    # Validate command line arguments
    if len(sys.argv) != 3:
        print("Usage: python generate.py <num_schedules> <complexity>")
        print("Example: python generate.py 5 3  # Generates 5 schedules with 3 operations each")
        sys.exit(1)

    try:
        num_schedules = int(sys.argv[1])
        complexity = int(sys.argv[2])
        
        if num_schedules <= 0 or complexity <= 0:
            raise ValueError("Both arguments must be positive integers")
            
        print(f"Generating {num_schedules} schedules with complexity {complexity}")
        generate_multiple_schedules(num_schedules, complexity)
        print(f"\nSuccessfully generated {num_schedules} schedules in the 'complex' directory")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Both arguments must be positive integers")
        sys.exit(1) 