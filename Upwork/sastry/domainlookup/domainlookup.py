import subprocess, sys
import pandas as pd

def check_validity(domain: str = 'google.com') -> str:

    print(f"Checking validity of {domain}")

    lookup_command = "nslookup"

    if lookup_command == "whois":
        command = "whois {} | grep 'This query returned 0 objects'".format(domain)
    elif lookup_command == "nslookup":
        command = "nslookup {} | grep -i \"Can't find\"".format(domain)
    else:
        print("Invalid domain lookup command provided. Exiting...")
        sys.exit() 

    command_output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    if "Non-authoritative" in str(command_output.stderr):
        return "available"
    else:
        return "unavailable"

data = pd.read_csv("domain_list.csv", header = None)
df = pd.DataFrame()

for idx, word in enumerate(data[0]):
    df.at[idx,"word"] = word
    base = word.replace(" ", "").lower()
    df.at[idx,"validity"] = check_validity(domain = f"{base}.com")

df.to_csv("domain_list_validities.csv", index = False)


