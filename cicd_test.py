#!/usr/bin/env python3
import subprocess
import os

def run_command(command, description=""):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if description:
            print(f"{description}: {result.returncode == 0}")
        return result
    except Exception as e:
        print(f"Error running command '{command}': {e}")
        return None

def main():
    print("Starting CI/CD test script...")

    # Initialize a new Git repository
    print("\n1. Initializing Git repository...")
    result = run_command("git init", "Git init")
    if result and result.returncode == 0:
        print("Git repository initialized successfully")

    # Create example.py file with Hello World
    print("\n2. Creating example.py file...")
    try:
        with open('example.py', 'w') as f:
            f.write("print('Hello World')\n")
        print("example.py created successfully")
    except Exception as e:
        print(f"Error creating example.py: {e}")
        return

    # Add the file to Git
    print("\n3. Adding example.py to Git...")
    result = run_command("git add example.py", "Git add")
    if result and result.returncode == 0:
        print("example.py added to staging area")

    # Commit the file
    print("\n4. Committing the file...")
    result = run_command('git commit -m "Initial commit"', "Git commit")
    if result and result.returncode == 0:
        print("File committed successfully")

    # Get Git status and log it to git_log.txt
    print("\n5. Logging Git status to git_log.txt...")
    status_result = run_command("git status", "Git status")
    if status_result:
        try:
            with open('git_log.txt', 'w') as f:
                f.write("Git Status Log\n")
                f.write("=" * 50 + "\n")
                f.write(f"Return code: {status_result.returncode}\n")
                f.write("STDOUT:\n")
                f.write(status_result.stdout)
                f.write("\nSTDERR:\n")
                f.write(status_result.stderr)
            print("Git status logged to git_log.txt successfully")
        except Exception as e:
            print(f"Error writing to git_log.txt: {e}")

    print("\nCI/CD test script completed!")

if __name__ == "__main__":
    main()