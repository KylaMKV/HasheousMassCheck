from sys import argv
import json
import subprocess
import requests as rq

program = argv[0]
args = argv[1:]
print(program)
# Create the log file before opening in append mode
#open("log.txt", "w").close()

with open("log.txt", "r") as fl:
    for line in fl.readlines():
        data = line.split("\t")
        if data[0] in args:
            args.remove(data[0])
            print(f"Skipping '{data[0]}'. Information already exists in 'log.txt'.")


log = open("log.txt", "a")

for arg in args:
    if arg == program:
        print(f"Skipping self({program})")
        continue
    checksum = subprocess.check_output(f"sha256sum \"{arg}\"", shell=True, text=True).split(" ")[0]
    print(arg)
    response = rq.get(f"https://hasheous.org/api/v1/Lookup/ByHash/sha256/{checksum}")
    report = "NOT FOUND"
    info = None 
    if response.status_code == 200:
        info = json.loads(response.text)
        # Redump so it's all in one line
        report = json.dumps(info)
        print(arg + "\t" + info["name"])
    else:
        print(arg + "\t" + "NOT FOUND")
    log.write(arg + "\t" + report + "\n")
