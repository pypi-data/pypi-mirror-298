Here’s the updated README with your additional installation steps for creating an environment and using the feroxbuster-cli package:
 
Feroxbuster Automation Script
This Python script automates the process of downloading, extracting, and running Feroxbuster against a target URL using a wordlist for content discovery. It handles downloading the Feroxbuster binary, unzipping it, and fetching the wordlist from a popular repository.
 
Features
Automatically downloads the latest version of Feroxbuster.
Unzips the Feroxbuster binary.
Downloads the common.txt wordlist from SecLists.
Runs Feroxbuster with the provided URL and wordlist.
Requirements
Python 3.x
Internet connection (for downloading Feroxbuster and the wordlist)
Windows operating system (as this downloads the Windows-specific executable for Feroxbuster)
 
 
Installation Steps
Step 1: Create a Python Virtual Environment
First, create a virtual environment to isolate dependencies:
python -m venv venv
Activate the environment:
venv\Scripts\activate
Step 2: Install feroxbuster-cli package
In the activated virtual environment, run:
pip install feroxbuster-cli
Step 3: Navigate to feroxbuster_cli Folder
Locate the feroxbuster_cli folder and navigate into it:
cd venv/Lib/site-packages/feroxbuster_cli/
Step 4: Install Required Libraries
Ensure that the requests library is installed by running:
pip install requests and pip install setuptools
Step 5: Run the Script
You can now run the Python script:
python cli.py
 
Usage
After installation, the script will:
Download the latest Feroxbuster binary.
Fetch the common.txt wordlist from the SecLists repository.
Execute Feroxbuster with the specified URL and wordlist.
 
 
Disclaimer
This script is designed to automate the setup and execution of Feroxbuster. Always ensure you have permission to run content discovery scans on a target website. Unauthorized use could result in legal consequences.