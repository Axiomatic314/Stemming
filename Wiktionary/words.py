import json
import sys

PRINT_WORDS = False
PRINT_STEMS = False
PRINT_STEM_PAIRS = False
PRINT_STEM_GROUPS = True
SIMPLIFY_STEM_GROUPS = True

def process_words(words):    
    word_replacements = list()
    word_groupings = dict()

    for word in words:
        if "etymology_templates" not in word.keys():
            continue

        #If the word is a person's name, we leave it as it is
        #If it is a multiword term, do not break it up
        ignore = False
        if "categories" in word.keys():
            for category in word["categories"]:
                if category.find("surnames") > -1 or category.find("given names") > -1 or category.find("multiword") > -1:
                    ignore = True
                    break
        if ignore: continue

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

            #Deal with any other language codes
            if "lang1" in template["args"] and template["args"]["lang1"] not in valid_lang_codes: continue
            if "lang2" in template["args"] and template["args"]["lang2"] not in valid_lang_codes: continue

            #Skip entries that include brackets, numbers, anything that isn't ASCII
            part1 = template["args"]["2"].lower()
            part2 = template["args"]["3"].lower()
            if not part1.isascii() or not part2.isascii():
                continue

            isValid = True
            for c in part1:
                if not c.isalpha() and c != "-":
                    isValid = False
                    break
            if not isValid: continue
            for c in part1:
                if not c.isalpha() and c != "-":
                    isValid = False
                    break
            if not isValid: continue

            #Skip words that start/end with hyphens
            if word["word"].startswith("-") or word["word"].endswith("-"): continue
            
            #Process the template     
            negative_suffixes = ["n't", "less", "-n't", "-less"]
            name = template["name"]
            if name == "affix" or name == "af":
                if part2.startswith("-") and not part1.endswith("-"): #suffix
                    if part2 not in negative_suffixes and not part1.startswith("-"): 
                        word_replacements.append((word["word"].lower(), part1))
                        if part1 in word_groupings.keys():
                            if word["word"] not in word_groupings[part1]:
                                word_groupings[part1].append(word["word"].lower())
                        else:
                            word_groupings[part1] = list()
                            word_groupings[part1].append(word["word"].lower())
            if name == "suffix" or name == "suf":
                if part2 not in negative_suffixes and not part1.startswith("-") and not part1.endswith("-"):
                    word_replacements.append((word["word"].lower(), part1))
                    if part1 in word_groupings.keys():
                        if word["word"] not in word_groupings[part1]:
                            word_groupings[part1].append(word["word"].lower())
                    else:
                        word_groupings[part1] = list()
                        word_groupings[part1].append(word["word"].lower())

    word_replacements.sort(key=lambda x: x[0])

    if SIMPLIFY_STEM_GROUPS:
        word_replacements, word_groupings = merge_groups(word_replacements, word_groupings)

    word_replacements = dict(word_replacements)
    word_groupings = dict(sorted(word_groupings.items()))

    return word_replacements, word_groupings
       
def print_replacements(word_replacements):
    for word in word_replacements:
        print(word + " -> " + word_replacements[word])

def merge_groups(word_replacements, word_groupings):
    initial_groups = set(word_groupings.keys())
    for word in initial_groups:
        print(f"{word}{' '*80}", end="\r", file=sys.stderr)
        if word in word_replacements:
            stem = word_replacements[word]
            for variant in word_groupings[word]:
                word_replacements[variant] = stem
            word_groupings[stem].extend(word_groupings[word])
            word_groupings.pop(word)
    return word_replacements, word_groupings

def print_groupings(word_groupings):
    for word in word_groupings:
        print(word + ": ", end="")
        for variant in word_groupings[word]:
            print(variant, end=" ")
        print()

def output_stems(word_groupings):
    for stem in word_groupings.keys():
        print(stem)

def output_words(word_replacements):
    for word in word_replacements.keys():
        print(word)

def main():
    wiktionary_data = "raw-wiktextract-data.json"
    words = list()  #list of all the English words in the Wiktionary
    data: dict = None
    with open(wiktionary_data, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if "lang" in data.keys() and data["lang"] == "English":
                words.append(data)
    
    #word_replacements contains all the word -> stem mappings
    #word_groupings contains all the stem -> word groups
    word_replacements, word_groupings = process_words(words)

    if PRINT_STEM_PAIRS:
        print_replacements(word_replacements)
    if PRINT_STEM_GROUPS:
        print_groupings(word_groupings)
    if PRINT_STEMS:
        output_stems(word_groupings)
    if PRINT_WORDS:
        output_words(word_replacements)




    
if __name__ == "__main__":
    main()

