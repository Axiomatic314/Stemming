import json
import sys
import traceback
from tqdm import tqdm
import pickle
import os
from typing import Dict, List, Set

PRINT_WORDS = True
PRINT_STEMS = False
PRINT_STEM_PAIRS = True
PRINT_STEM_GROUPS = True
SIMPLIFY_STEM_GROUPS = True

def process_words(words):    
    word_to_stem = dict()
    word_clusters = dict()

    for word in tqdm(words):
        #Entry needs to have a word at all
        if "word" not in word.keys():
            continue
        
        #We HATE crustacea in this household
        if word["word"] == "crustacean": continue
        if word["word"] == "cow" : continue


        #Don't stem words under 3 characters long
        if len(word["word"]) <= 2:
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

        #Skip entries that include brackets, numbers, anything that isn't in the alphabet
        if not word["word"].isalpha() or not word["word"].isascii():
            continue

        if "etymology_templates" in word.keys():
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

                #Need to leave hyphens at the start/end in the affix entries for processing
                part1 = template["args"]["2"].lower()
                part2 = template["args"]["3"].lower()

                temp = part1
                if temp.startswith("-"): temp = temp[1:]
                if temp.endswith("-"): temp = temp[:-1]
                if not temp.isalpha() or not temp.isascii(): continue
                temp = part2
                if temp.startswith("-"): temp = temp[1:]
                if temp.endswith("-"): temp = temp[:-1]
                if not temp.isalpha() or not temp.isascii(): continue

                #Process the template
                word_lower = word["word"].lower()     
                negative_suffixes = ["n't", "less", "-n't", "-less"]
                name = template["name"]
                if name == "affix" or name == "af":
                    if part2.startswith("-") and not part1.endswith("-"): #suffix
                        if part2 not in negative_suffixes and not part1.startswith("-"):
                            if word_lower in word_to_stem: continue 
                            word_to_stem[word_lower] = part1
                            if part1 not in word_clusters.keys():
                                word_clusters[part1] = set()
                            word_clusters[part1].add(word_lower)
                if name == "suffix" or name == "suf":
                    if part2 not in negative_suffixes and not part1.startswith("-") and not part1.endswith("-"):
                        if word_lower in word_to_stem: continue
                        word_to_stem[word_lower] = part1
                        if part1 not in word_clusters.keys():
                            word_clusters[part1] = set()
                        word_clusters[part1].add(word_lower)
        #If the word is a participle/plural/etc. find the original word
        #Only take the first form from the first sense
        #Ignore if the entry is more than one word - could be a description
        elif "senses" in word.keys() and "tags" in word["senses"][0].keys():
            tags = word["senses"][0]["tags"]
            if "form-of" in tags and ("participle" in tags or "plural" in tags):
                word_lower = word["word"].lower()
                stem = word["senses"][0]["form_of"][0]["word"].lower()
                if not stem.isalpha() or not stem.isascii(): continue
                if word_lower in word_to_stem: continue
                word_to_stem[word_lower] = stem
                if stem not in word_clusters.keys():
                    word_clusters[stem] = set()
                word_clusters[stem].add(word_lower)

    if SIMPLIFY_STEM_GROUPS:
        print("Simplifying clusters...", file=sys.stderr)
        word_to_stem, word_clusters = merge_groups(word_to_stem, word_clusters)

    return word_to_stem, word_clusters
       
# def update_groups(initial_stem: str, word_to_stem: Dict[str,str], word_clusters: Dict[str, Set[str]]):
#     if initial_stem in word_to_stem.keys():
#         super_stem = word_to_stem[initial_stem]
#         for variant in word_clusters[initial_stem]:
#             word_to_stem[variant] = super_stem
#         word_clusters[super_stem].extend(word_clusters[initial_stem])
#         word_clusters.pop(initial_stem)

def merge_groups(word_to_stem: Dict[str, str], word_clusters: Dict[str, Set[str]]):
    initial_stems = set(word_clusters.keys())
    # Walk over all the stems proposed before merging
    total_stems = 0
    problem_stems = 0
    total_super_stems = 0
    for initial_stem in tqdm(initial_stems):
        total_stems+=1
        # If the stem is replaced by something else (a super-stem) we can merge it
        # update_groups(initial_stem, word_to_stem, word_clusters)
        if initial_stem in word_to_stem.keys():
            total_super_stems+=1
            super_stem = word_to_stem[initial_stem]
            for variant in word_clusters[initial_stem]:
                word_to_stem[variant] = super_stem
            try:
                initial_stem_cluster = word_clusters[initial_stem]
                word_clusters[super_stem].update(initial_stem_cluster)
                word_clusters.pop(initial_stem)
            except KeyError as e:
                problem_stems+=1
                traceback.print_exc()
                print(f"{e} => {initial_stem} -> {super_stem}")
    print(f"Total stems: {total_stems}\nTotal super stems: {total_super_stems}\nTotal problem stems: {problem_stems}")
    return word_to_stem, word_clusters

def print_replacements(word_to_stem, filename):
    sorted_words = sorted(set(word_to_stem.keys()))
    with open(filename, "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + " -> " + word_to_stem[word] + "\n")

def print_clusters(word_clusters, filename):
    with open(filename, "w", encoding="utf-8") as f:
        sorted_stems = sorted(set(word_clusters.keys()))
        for stem in sorted_stems:
            f.write(stem)
            for variant in word_clusters[stem]:
                f.write(" " + variant)
            f.write("\n")

def output_stems(word_clusters, filename):
    sorted_stems = sorted(set(word_clusters.keys()))
    with open(filename, "w", encoding="utf-8") as f:
        for stem in sorted_stems:
            f.write(stem + "\n")

def output_words(word_to_stem, filename):
    sorted_words = sorted(set(word_to_stem.keys()))
    with open(filename, "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")

def main():
    wiktionary_data = "Wiktionary/raw-wiktextract-data.json"
    words = list()  #list of all the English words in the Wiktionary
    data: dict = None
    print("Reading Wiktionary data...", file=sys.stderr)
    if not os.path.exists("Wiktionary/words.pkl"):
        with open(wiktionary_data, "r", encoding="utf-8") as f:
            for line in tqdm(f):
                data = json.loads(line)
                if "lang" in data.keys() and data["lang"] == "English":
                    words.append(data)
        with open("Wiktionary/words.pkl", "wb") as f:
            pickle.dump(words, f)
    else:
        with open("Wiktionary/words.pkl", "rb") as f:
            words = pickle.load(f)
    #word_to_stem contains all the word -> stem mappings
    #word_clusters contains all the stem -> word groups
    print("Processing Wiktionary words...", file=sys.stderr)
    word_to_stem, word_clusters = process_words(words)

    if PRINT_STEM_PAIRS:
        print("Writing word -> stem to file...", file=sys.stderr)
        print_replacements(word_to_stem, "Wiktionary/wordToStem.txt")
    if PRINT_STEM_GROUPS:
        print("Writing clusters to file...", file=sys.stderr)
        print_clusters(word_clusters, "Wiktionary/clusters.txt")
    if PRINT_STEMS:
        print("Writing stems to file...", file=sys.stderr)
        output_stems(word_clusters, "Wiktionary/stems.txt")
    if PRINT_WORDS:
        print("Writing words to file...", file=sys.stderr)
        output_words(word_to_stem, "Wiktionary/words.txt")
    print("Complete!", file=sys.stderr)



    
if __name__ == "__main__":
    main()

