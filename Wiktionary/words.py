import json

filename = "raw-wiktextract-data.json"
data: dict = None

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        #Process the data accordingly
        #For example:
        if "lang" in data.keys():
            if data["lang"] != "English": print(data["lang"])