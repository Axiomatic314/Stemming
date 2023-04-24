import json

filename = "raw-wiktextract-data.json"
words = list() #list of all the English words in the Wiktionary
word_variants = list() #contains all the word:replacment pairs

data: dict = None
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if "lang" in data.keys() and data["lang"] == "English":
            words.append(data)
            
for word in words:
    if "etymology_templates" not in word.keys():
        continue

    #If the word is a person's name, we leave it as it is
    #If it is a multiword term, do not break it up
    remove = False
    if "categories" in word.keys():
        for category in word["categories"]:
            if category.find("surnames") > -1 or category.find("given names") > -1 or category.find("multiword") > -1:
                remove = True
                break
    if remove: continue

    for template in word["etymology_templates"]:
        valid_lang_codes = ["en"]
        if "1" in template["args"] and template["args"]["1"] not in valid_lang_codes:
            continue
 
        #Only process the entry if the main word components are provided
        if "2" not in template["args"] or "3" not in template["args"]:
            continue
        if len(template["args"]["2"]) == 0 or len(template["args"]["3"]) == 0:
            continue
        if template["args"]["2"] == "?" or template["args"]["3"] == "?":
            continue

        #Deal with any language codes included in the word components
        temp = template["args"]["2"].split(":")
        if len(temp) > 1:
            if temp[0] not in valid_lang_codes:
                continue
            template["args"]["2"] = temp[1]
        temp = template["args"]["3"].split(":")
        if len(temp) > 1:
            if temp[0] not in valid_lang_codes:
                continue
            template["args"]["3"] = temp[1]
        if "<" in template["args"]["2"] or "<" in template["args"]["3"]:
            continue
            
        #Process the template    
        negative_prefixes = ["anti", "anti-", "ab", "ab-", "non", "non-", "un", "un-"] #not exahustive
        negative_suffixes = ["n't", "n't-"]
        name = template["name"]
        part1 = template["args"]["2"]
        part2 = template["args"]["3"]
        if name == "affix" or name == "af":
            if part1.endswith("-") and not part2.startswith("-"): #prefix
                if part1 not in negative_prefixes:
                    word_variants.append((word["word"], part2))
            elif part2.startswith("-") and not part1.endswith("-"): #suffix
                if part2 not in negative_suffixes: 
                    word_variants.append((word["word"], part1))
        if name == "prefix" or name == "pre":
            if part1 not in negative_prefixes:
                word_variants.append((word["word"], part2))
        if name == "suffix" or name == "suf":
            if part2 not in negative_suffixes:
                word_variants.append((word["word"], part1))
       

word_variants.sort(key=lambda x: x[1])
for word in word_variants:
    print(word[0] + ": " + word[1])