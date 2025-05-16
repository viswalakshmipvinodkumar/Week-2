# Script to output numbers from 1 to 200

def main():
    # Open a file to write the numbers
    with open('numbers.txt', 'w') as file:
        # Loop from 1 to 200
        for i in range(1, 201):
            # Write each number to the file
            file.write(str(i) + '\n')
            # Also print to console
            print(i)

if __name__ == "__main__":
    main()
