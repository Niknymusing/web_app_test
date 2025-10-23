#!/usr/bin/env python3
"""
CI/CD Full Test Script
Generates FastAPI app, tests, runs tests, and pushes to Git repository.
"""

import os
import sys
import subprocess
import datetime
import json
import shutil
from pathlib import Path

def log_to_file(message, filename="git_log.txt"):
    """Log messages to a file with timestamp."""
    timestamp = datetime.datetime.now().isoformat()
    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def run_command(cmd, capture_output=True, log_output=True):
    """Run a command and optionally log the output."""
    log_to_file(f"Running command: {cmd}")
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        else:
            result = subprocess.run(cmd, capture_output=capture_output, text=True)

        if log_output:
            if result.stdout:
                log_to_file(f"STDOUT: {result.stdout}")
            if result.stderr:
                log_to_file(f"STDERR: {result.stderr}")
            log_to_file(f"Return code: {result.returncode}")

        return result
    except Exception as e:
        log_to_file(f"Command failed with exception: {str(e)}")
        return None

def generate_fastapi_app():
    """Generate a simple FastAPI app with /hello endpoint."""
    print("Generating FastAPI app...")

    app_content = '''from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/hello")
def read_hello():
    timestamp = datetime.datetime.now().isoformat()
    return f"Hello, World! - Test {timestamp}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    with open("app.py", "w") as f:
        f.write(app_content)

    print("✓ Generated app.py")
    log_to_file("Generated app.py with FastAPI /hello endpoint")

def generate_pytest_test():
    """Generate pytest test for the /hello endpoint."""
    print("Generating pytest test...")

    test_content = '''import sys
sys.path.insert(0, '.')

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_hello_endpoint():
    """Test the /hello endpoint returns the expected format."""
    response = client.get("/hello")
    assert response.status_code == 200

    # Use response.json() for the assertion as requested (handle string response)
    response_data = response.json()

    # The FastAPI endpoint returns a string, so response.json() gives us the string directly
    assert isinstance(response_data, str)
    assert response_data.startswith("Hello, World! - Test ")

    # Verify timestamp format is present (basic check)
    assert "T" in response_data  # ISO format contains 'T'

    print(f"Test passed! Response: {response_data}")
'''

    with open("test_app.py", "w") as f:
        f.write(test_content)

    print("✓ Generated test_app.py")
    log_to_file("Generated test_app.py with pytest test for /hello endpoint")

def run_tests():
    """Run the pytest tests directly (skip pip install since deps are available)."""
    print("Running tests...")
    log_to_file("Starting pytest execution")

    # Run pytest directly as requested (skip pip install since deps are already available)
    test_result = run_command("pytest test_app.py -v")

    if test_result and test_result.returncode == 0:
        print("✓ All tests passed!")
        log_to_file("All tests passed successfully")
        return True
    else:
        print("✗ Tests failed!")
        log_to_file("Tests failed")
        if test_result:
            print(f"Test output: {test_result.stdout}")
            print(f"Test errors: {test_result.stderr}")
        return False

def setup_git_repo():
    """Initialize a fresh Git repository."""
    print("Setting up Git repository...")

    # Remove existing .git if it exists
    if os.path.exists(".git"):
        shutil.rmtree(".git")
        log_to_file("Removed existing .git directory")

    # Initialize new repo
    run_command("git init")
    run_command('git config user.email "test@example.com"')
    run_command('git config user.name "Test User"')

    print("✓ Initialized fresh Git repository")
    log_to_file("Initialized fresh Git repository")

def commit_and_push():
    """Add files, commit, and push to remote repository."""
    print("Committing and pushing to repository...")

    # Get environment variables
    git_repo_url = os.getenv("GIT_REPO_URL")
    github_token = os.getenv("GITHUB_TOKEN")

    if not git_repo_url:
        print("⚠️  GIT_REPO_URL environment variable not set, using placeholder")
        log_to_file("WARNING: GIT_REPO_URL environment variable not set, using placeholder")
        git_repo_url = "https://github.com/user/repo.git"

    if not github_token:
        print("⚠️  GITHUB_TOKEN environment variable not set, using placeholder")
        log_to_file("WARNING: GITHUB_TOKEN environment variable not set, using placeholder")
        github_token = "placeholder_token"

    # Add all files
    run_command("git add .")

    # Create commit with timestamp
    timestamp = datetime.datetime.now().isoformat()
    commit_message = f"Initial app commit - {timestamp}"
    run_command(f'git commit -m "{commit_message}"')

    # Set up remote with authentication using the format: https://oauth2:$GITHUB_TOKEN@github.com/repo.git
    if "github.com" in git_repo_url:
        # Extract the repo part from the URL
        repo_part = git_repo_url.replace("https://github.com/", "").replace("http://github.com/", "")
        auth_url = f"https://oauth2:{github_token}@github.com/{repo_part}"
    else:
        # For other git providers, use basic format
        auth_url = git_repo_url.replace("https://", f"https://oauth2:{github_token}@")

    run_command(f"git remote add origin {auth_url}")

    # Check current branch and push to master with force as requested
    print("Pushing to remote repository...")
    run_command("git branch -M master")
    push_result = run_command("git push -f -u origin master")

    # Log detailed push output and any auth errors
    if push_result:
        log_to_file(f"Push return code: {push_result.returncode}")
        if push_result.stdout:
            log_to_file(f"Push detailed output: {push_result.stdout}")
        if push_result.stderr:
            log_to_file(f"Push detailed errors: {push_result.stderr}")

        # Check for auth errors specifically
        if push_result.stderr:
            stderr_lower = push_result.stderr.lower()
            if "authentication failed" in stderr_lower or "401" in stderr_lower:
                log_to_file("AUTH ERROR: Authentication failed - check GITHUB_TOKEN")
                print("🔐 Authentication error detected. Check GITHUB_TOKEN environment variable.")
            elif "repository not found" in stderr_lower or "404" in stderr_lower:
                log_to_file("AUTH ERROR: Repository not found - check GIT_REPO_URL")
                print("📂 Repository not found. Check GIT_REPO_URL environment variable.")
            elif "permission denied" in stderr_lower or "403" in stderr_lower:
                log_to_file("AUTH ERROR: Permission denied - check repository permissions")
                print("🚫 Permission denied. Check repository permissions and token scope.")

    if push_result and push_result.returncode == 0:
        print("✓ Successfully pushed to remote repository!")
        log_to_file("Successfully pushed to remote repository")
        return True
    else:
        print("✗ Failed to push to remote repository (check git_log.txt for details)")
        log_to_file("Failed to push to remote repository")
        return False

def main():
    """Main execution function."""
    print("=" * 50)
    print("CI/CD Full Test Pipeline Starting")
    print("=" * 50)

    # Clear previous log
    if os.path.exists("git_log.txt"):
        os.remove("git_log.txt")

    log_to_file("Starting CI/CD Full Test Pipeline")

    try:
        # Step 1: Generate FastAPI app
        generate_fastapi_app()

        # Step 2: Generate pytest test
        generate_pytest_test()

        # Step 3: Run tests
        if not run_tests():
            print("Tests failed. Stopping pipeline.")
            return 1

        # Step 4: Setup Git and commit/push
        setup_git_repo()

        if not commit_and_push():
            print("Git operations failed. Pipeline completed with errors.")
            return 1

        print("\n" + "=" * 50)
        print("✓ CI/CD Pipeline completed successfully!")
        print("=" * 50)
        log_to_file("CI/CD Pipeline completed successfully")

        return 0

    except Exception as e:
        print(f"Pipeline failed with exception: {str(e)}")
        log_to_file(f"Pipeline failed with exception: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)