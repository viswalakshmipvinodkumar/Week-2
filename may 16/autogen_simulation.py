"""
AutoGen Simulation - Demonstrates the structure without API calls

This script simulates the behavior of AutoGen agents without requiring an API key.
It follows the same flow as the reference video example.
"""

import os
import time

# Create the web directory if it doesn't exist
os.makedirs("web", exist_ok=True)

def simulate_cto_response(task):
    """Simulate responses from the CTO agent"""
    print("\n=== CTO Agent ===")
    
    if "output numbers 1 to 100" in task:
        # Simulate thinking
        print("Thinking...")
        time.sleep(1)
        
        # First response - code generation
        response = """I'll write a Python script to output numbers 1 to 100 and save it to a file.

```python
# Script to output numbers from 1 to 100

def main():
    # Open a file to write the numbers
    with open('numbers.txt', 'w') as file:
        # Loop from 1 to 100
        for i in range(1, 101):
            # Write each number to the file
            file.write(str(i) + '\\n')
            # Also print to console
            print(i)

if __name__ == "__main__":
    main()
```

I'll save this to a file called `numbers.py`. This script will:
1. Create a function called `main()`
2. Open a file called `numbers.txt` in write mode
3. Loop from 1 to 100
4. Write each number to the file and print it to the console
5. Call the `main()` function when the script is executed

Would you like me to execute this code?"""
        
        print(response)
        
        # Simulate file creation
        with open("web/numbers.py", "w") as f:
            f.write("""# Script to output numbers from 1 to 100

def main():
    # Open a file to write the numbers
    with open('numbers.txt', 'w') as file:
        # Loop from 1 to 100
        for i in range(1, 101):
            # Write each number to the file
            file.write(str(i) + '\\n')
            # Also print to console
            print(i)

if __name__ == "__main__":
    main()
""")
        
        return response
        
    elif "output numbers 1 to 200" in task:
        # Simulate thinking
        print("Thinking...")
        time.sleep(1)
        
        # Response for the second task
        response = """I'll modify the existing Python script to output numbers 1 to 200 instead of 1 to 100.

```python
# Script to output numbers from 1 to 200

def main():
    # Open a file to write the numbers
    with open('numbers.txt', 'w') as file:
        # Loop from 1 to 200 (modified from 100)
        for i in range(1, 201):
            # Write each number to the file
            file.write(str(i) + '\\n')
            # Also print to console
            print(i)

if __name__ == "__main__":
    main()
```

I've updated the code to:
1. Change the comment to reflect the new range (1 to 200)
2. Modify the loop range from `range(1, 101)` to `range(1, 201)`

The rest of the functionality remains the same. The script will:
1. Open a file called `numbers.txt` in write mode
2. Loop from 1 to 200
3. Write each number to the file and print it to the console

Would you like me to execute this updated code?"""
        
        print(response)
        
        # Simulate file update
        with open("web/numbers.py", "w") as f:
            f.write("""# Script to output numbers from 1 to 200

def main():
    # Open a file to write the numbers
    with open('numbers.txt', 'w') as file:
        # Loop from 1 to 200
        for i in range(1, 201):
            # Write each number to the file
            file.write(str(i) + '\\n')
            # Also print to console
            print(i)

if __name__ == "__main__":
    main()
""")
        
        return response
    
    else:
        return "I'm not sure how to respond to that task."

def simulate_user_proxy_response(cto_response, task_number):
    """Simulate responses from the user proxy agent"""
    print("\n=== User Proxy Agent ===")
    
    if "Would you like me to execute this code?" in cto_response:
        print("Yes, please execute the code.")
        
        # Simulate code execution
        print("\n=== Executing Code ===")
        time.sleep(1)
        
        # Execute the actual Python script
        os.system("cd web && python numbers.py > output.txt")
        
        print("Code executed successfully.")
        print("Created file: web/numbers.txt with numbers 1 to 100")
        
        # First task response
        print("\nCONTINUE")
        return "CONTINUE"
        
    elif "Would you like me to execute this updated code?" in cto_response:
        print("Yes, please execute the updated code.")
        
        # Simulate code execution
        print("\n=== Executing Updated Code ===")
        time.sleep(1)
        
        # Execute the actual Python script
        os.system("cd web && python numbers.py > output.txt")
        
        print("Code executed successfully.")
        print("Updated file: web/numbers.txt with numbers 1 to 200")
        
        # Final task response
        print("\nTERMINATE")
        return "TERMINATE"
    
    else:
        return "I'm not sure how to respond."

def main():
    print("\n" + "=" * 60)
    print("AUTOGEN SIMULATION - FOLLOWING THE REFERENCE VIDEO")
    print("=" * 60)
    
    # Task 1: Write code to output numbers 1 to 100
    print("\n" + "=" * 60)
    print("TASK 1: Write python code to output numbers 1 to 100, and then store the code in a file")
    print("=" * 60)
    
    task1 = "Write python code to output numbers 1 to 100, and then store the code in a file"
    
    # Simulate the chat for Task 1
    cto_response = simulate_cto_response(task1)
    user_response = simulate_user_proxy_response(cto_response, 1)
    
    # Task 2: Modify the code to output numbers 1 to 200
    print("\n" + "=" * 60)
    print("TASK 2: Change the code in the file you just created to instead output numbers 1 to 200")
    print("=" * 60)
    
    task2 = "Change the code in the file you just created to instead output numbers 1 to 200"
    
    # Simulate the chat for Task 2
    cto_response = simulate_cto_response(task2)
    user_response = simulate_user_proxy_response(cto_response, 2)
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
    
    print("\nFiles created in the 'web' directory:")
    print("- numbers.py: The Python script that outputs numbers")
    print("- numbers.txt: The file containing the numbers from 1 to 200")
    print("- output.txt: The console output from running the script")
    
    print("\nYou can examine these files to see the results of the simulation.")

if __name__ == "__main__":
    main()
