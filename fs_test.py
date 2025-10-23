#!/usr/bin/env python3

def main():
    # Create and write to test.txt
    with open('test.txt', 'w') as f:
        f.write('Hello, MEU Agent!')

    # Read the file content
    with open('test.txt', 'r') as f:
        content = f.read()

    # Log the content to read_log.txt
    with open('read_log.txt', 'w') as f:
        f.write(f"Content read from test.txt: {content}\n")

    print(f"Successfully created test.txt with content: {content}")
    print("Content logged to read_log.txt")

if __name__ == "__main__":
    main()