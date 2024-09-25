# Feroxbuster Automation Script

This Python script automates the process of downloading, extracting, and running [Feroxbuster](https://github.com/epi052/feroxbuster) against a target URL using a wordlist for content discovery. It handles downloading the Feroxbuster binary, unzipping it, and fetching the wordlist from a popular repository.

## Features

- Automatically downloads the latest version of Feroxbuster.
- Unzips the Feroxbuster binary.
- Downloads the `common.txt` wordlist from [SecLists](https://github.com/danielmiessler/SecLists).
- Runs Feroxbuster with the provided URL and wordlist.

## Requirements

- Python 3.x
- Internet connection (for downloading Feroxbuster and the wordlist)
- Windows operating system (as this downloads the Windows-specific executable for Feroxbuster)

## Installation

1. Clone the repository or download the script files.

2. Install the required Python packages:

   ```bash
   pip install requests
   
   python script_name.py
