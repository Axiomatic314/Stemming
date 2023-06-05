import json
import sys
from tqdm import tqdm

PRINT_WORDS = True
PRINT_STEMS = False
PRINT_STEM_PAIRS = True
PRINT_STEM_GROUPS = True
SIMPLIFY_STEM_GROUPS = True

def process_words(words):    
    word_replacements = list()
    word_clusters = dict()

    for word in tqdm(words):
        if "word" in word.keys() and len(word["word"]) <= 2:
            continue

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

            #Skip entries that include brackets, numbers, anything that isn't in the alphabet
            if not word["word"].isalpha():
                continue

            #Need to leave hyphens at the start/end in the affix entries for processing
            part1 = template["args"]["2"].lower()
            part2 = template["args"]["3"].lower()

            temp = part1
            if temp.startswith("-"): temp = temp[1:]
            if temp.endswith("-"): temp = temp[:-1]
            if not temp.isalpha(): continue
            temp = part2
            if temp.startswith("-"): temp = temp[1:]
            if temp.endswith("-"): temp = temp[:-1]
            if not temp.isalpha(): continue
            
            #Process the template
            word_lower = word["word"].lower()     
            negative_suffixes = ["n't", "less", "-n't", "-less"]
            name = template["name"]
            if name == "affix" or name == "af":
                if part2.startswith("-") and not part1.endswith("-"): #suffix
                    if part2 not in negative_suffixes and not part1.startswith("-"): 
                        word_replacements.append((word_lower, part1))
                        if part1 not in word_clusters.keys():
                            word_clusters[part1] = list()
                        if word_lower not in word_clusters[part1]:
                            word_clusters[part1].append(word_lower)
            if name == "suffix" or name == "suf":
                if part2 not in negative_suffixes and not part1.startswith("-") and not part1.endswith("-"):
                    word_replacements.append((word_lower, part1))
                    if part1 not in word_clusters.keys():
                        word_clusters[part1] = list()
                    if word_lower not in word_clusters[part1]:
                        word_clusters[part1].append(word_lower)

    word_replacements.sort(key=lambda x: x[0])
    word_replacements = dict(word_replacements)

    if SIMPLIFY_STEM_GROUPS:
        print("Simplifying clusters...", file=sys.stderr)
        word_replacements, word_clusters = merge_groups(word_replacements, word_clusters)

    # word_replacements = dict(word_replacements)
    word_clusters = dict(sorted(word_clusters.items()))

    return word_replacements, word_clusters
       
def print_replacements(word_replacements, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for word in word_replacements:
            f.write(word + " -> " + word_replacements[word] + "\n")

def merge_groups(word_replacements, word_clusters):
    initial_groups = set(word_clusters.keys())
    for word in tqdm(initial_groups):
        if word in word_replacements.keys():
            stem = word_replacements[word]
            for variant in word_clusters[word]:
                word_replacements[variant] = stem
            word_clusters[stem].extend(word_clusters[word])
            word_clusters.pop(word)
    return word_replacements, word_clusters

def print_clusters(word_clusters, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for word in word_clusters:
            f.write(word)
            for variant in word_clusters[word]:
                f.write(" " + variant)
            f.write("\n")

def output_stems(word_clusters, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for stem in word_clusters.keys():
            f.write(stem + "\n")

def output_words(word_replacements, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for word in word_replacements.keys():
            f.write(word + "\n")

def main():
    wiktionary_data = "Wiktionary/raw-wiktextract-data.json"
    words = list()  #list of all the English words in the Wiktionary
    data: dict = None
    print("Reading Wiktionary data...", file=sys.stderr)
    with open(wiktionary_data, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            data = json.loads(line)
            if "lang" in data.keys() and data["lang"] == "English":
                words.append(data)
    
    #word_replacements contains all the word -> stem mappings
    #word_clusters contains all the stem -> word groups
    print("Processing Wiktionary words...", file=sys.stderr)
    word_replacements, word_clusters = process_words(words)

    if PRINT_STEM_PAIRS:
        print("Writing word -> stem to file...", file=sys.stderr)
        print_replacements(word_replacements, "Wiktionary/replacements.txt")
    if PRINT_STEM_GROUPS:
        print("Writing clusters to file...", file=sys.stderr)
        print_clusters(word_clusters, "Wiktionary/clusters.txt")
    if PRINT_STEMS:
        print("Writing stems to file...", file=sys.stderr)
        output_stems(word_clusters, "Wiktionary/stems.txt")
    if PRINT_WORDS:
        print("Writing words to file...", file=sys.stderr)
        output_words(word_replacements, "Wiktionary/words.txt")
    print("Complete!", file=sys.stderr)



    
if __name__ == "__main__":
    main()

