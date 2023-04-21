import json

filename = "raw-wiktextract-data.json"
data: dict = None
words = list()

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if "lang" in data.keys() and data["lang"] == "English":
            words.append(data)

for word in words:
    if "etymology_templates" not in word.keys():
        continue
    for template in word["etymology_templates"]:
        name = template["name"]
        if name == "affix" or name == "af":
            print(word["word"] + " ")
            for arg in template["args"]:
                print(str(arg) + " " + template["args"][arg])