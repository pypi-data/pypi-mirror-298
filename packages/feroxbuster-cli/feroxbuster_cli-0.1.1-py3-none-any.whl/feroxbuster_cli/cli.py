import os
import requests
import zipfile
import subprocess

def download_feroxbuster():
    print("Downloading Feroxbuster...")
    url = "https://github.com/epi052/feroxbuster/releases/latest/download/x86_64-windows-feroxbuster.exe.zip"
    response = requests.get(url)
    with open("feroxbuster.zip", "wb") as f:
        f.write(response.content)
    print("Download complete!")

def unzip_feroxbuster():
    print("Unzipping Feroxbuster...")
    with zipfile.ZipFile("feroxbuster.zip", "r") as zip_ref:
        zip_ref.extractall("feroxbuster")
    print("Unzipping complete!")

def run_feroxbuster(url, wordlist_path):
    feroxbuster_path = os.path.join("feroxbuster", "feroxbuster.exe")
    command = f'{feroxbuster_path} -u {url} -w {wordlist_path}'
    print(f"Running Feroxbuster: {command}")
    subprocess.run(command, shell=True)

def main():
    if not os.path.exists("feroxbuster"):
        download_feroxbuster()
        unzip_feroxbuster()

    url = input("Enter the URL of the website: ")

    wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/common.txt"
    wordlist_path = "common.txt"

    if not os.path.exists(wordlist_path):
        print("Downloading wordlist...")
        wordlist_response = requests.get(wordlist_url)
        with open(wordlist_path, "wb") as f:
            f.write(wordlist_response.content)
        print("Wordlist downloaded.")

    run_feroxbuster(url, wordlist_path)

if __name__ == "__main__":
    main()
