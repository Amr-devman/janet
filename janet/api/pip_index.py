import json
import subprocess
from datetime import datetime

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def populate():
    print("Populating your local PIP index for faster searches")
    index_json= {}

    cmd = ["wget", "-O", "index.html", "https://pypi.org/simple/"]
    subprocess.run(cmd)

    with open("index.html", "r") as index:
        parsed_html = BeautifulSoup(index)
        packages = parsed_html.body.find_all('a')
        
        for package in packages:
            package_name = package[package.index('">')+2:package.index('</')]

            curr_time = datetime.now()
		    curr_time = curr_time.strftime("%m-%d-%Y-%H--%M--%S")

            index_json[package_name] = curr_time

    with open("index.json", "w") as local_index:
        json.dump(index_json,local_index, indent=4)

    

def search(package):
    with open("index.json") as index_file:
        index = json.load(index_file)

    if package in index:
        return True
    else:
        False



