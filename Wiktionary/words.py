import json

filename = "raw-wiktextract-data.json"
data: dict = None
words = list()
word_variants = dict()

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
        if "1" in template["args"] and template["args"]["1"] != "en":
            continue
        #If there is an override code for a language that is not English, skip it
        #Deal with any language codes included in the components themselves
        if "2" in template["args"]:
            temp = template["args"]["2"].split(":")
            if len(temp) > 1 and temp[0] != "en": 
                continue
            elif len(temp) > 1:
                template["args"]["2"] = temp[1]
        if "3" in template["args"]:
            temp = template["args"]["3"].split(":")
            if len(temp) > 1 and temp[0] != "en": 
                continue
            elif len(temp) > 1:
                template["args"]["3"] = temp[1]
        #Obtain the root if able
        if name == "affix" or name == "af":
            if "2" in template["args"] and "3" in template["args"]:
                if template["args"]["2"].endswith("-") and not template["args"]["3"].startswith("-"): #prefix
                    word_variants[word["word"]] = template["args"]["3"]
                elif template["args"]["3"].startswith("-") and not template["args"]["2"].endswith("-"): #suffix
                    word_variants[word["word"]] = template["args"]["2"]
        if name == "prefix" or name == "pre":
            if "3" in template["args"]: 
                word_variants[word["word"]] = template["args"]["3"]
        if name == "suffix" or name == "suf":
            if "2" in template["args"]: 
                word_variants[word["word"]] = template["args"]["2"]

# for entry in word_variants:
#     print(entry + ": ", end="")
#     if len(word_variants[entry]) < 1:
#         print("\n")
#         continue
#     for variant in word_variants[entry]:
#         print(variant, sep=", ")

for word in word_variants:
    print(word + ": ", end="")
    print(word_variants[word])