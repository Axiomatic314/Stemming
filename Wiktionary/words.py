import json
import sys
import pickle
import os
from tqdm import tqdm
from typing import Dict, Set, List
import traceback

WIKT_DATA_RAW_FILE = "raw-wiktextract-data.json"
WIKT_DATA_EN_FILE = "raw-wiktextract-en.pkl"

PRINT_WORDS = True
PRINT_STEMS = False
PRINT_WORD_TO_STEM = True
PRINT_CLUSTERS = True
SIMPLIFY_CLUSTERS = True

def update_words(word_to_stem: Dict[str,str], word_clusters: Dict[str, Set[str]], word: str, stem: str):
    """
    Update the dictionaries with the given word and stem.
    """
    if word not in word_to_stem:
        word_to_stem[word] = stem
        if stem not in word_clusters.keys():
            word_clusters[stem] = set()
        word_clusters[stem].add(word)

    return word_to_stem, word_clusters

def process_words(wikt_data_en: List[Dict]):
    """
    Filter through the English words to extract their roots.
    """
    word_to_stem = dict()
    word_clusters = dict()

    valid_lang_codes = ["en"]
    negative_suffixes = ["n't", "less", "-n't", "-less"]

    for data in tqdm(wikt_data_en):
        #Entry needs to have a word at all
        if "word" not in data.keys():
            continue

        word = data["word"].lower()
    
        #Don't stem words under 3 characters long
        if len(word) <= 2: continue

        #Skip words that include brackets, numbers, anything that isn't a-z
        if not word.isalpha() or not word.isascii(): continue

        #Ignore problem words
        if word == "crustacean" : continue
        if word == "cow" : continue
        if word == "sagacity" : continue

        #If it is a multiword term, do not break it up
        ignore = False
        if "categories" in data.keys():
            for category in data["categories"]:
                if category.find("multiword") > -1:
                    ignore = True
                    break
        if ignore: continue

        #Ignore proper nouns
        if "pos" in data.keys() and data["pos"] == "name": continue

        #If the word has multiple etymologies, but the first didn't have useful information, ignore
        # if "etymology_number" in data.keys() and data["etymology_number"] > 1: continue
        
        #If the word has an etymology section, try to extract the root from the suffix/affix template
        if "etymology_templates" in data.keys() and len(data["etymology_templates"]) > 0:
            for template in data["etymology_templates"]:
                #Check if the template is actually in English
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

                #Actually process the template
                name = template["name"]
                if name == "affix" or name == "af":
                    if part2.startswith("-") and not part1.endswith("-"): #suffix
                        if part2 not in negative_suffixes and not part1.startswith("-"):
                            word_to_stem, word_clusters = update_words(word_to_stem, word_clusters, word, part1)
                if name == "suffix" or name == "suf":
                    if part2 not in negative_suffixes and not part1.startswith("-") and not part1.endswith("-"):
                        word_to_stem, word_clusters = update_words(word_to_stem, word_clusters, word, part1)
        #If the word is a participle/plural/etc. find the root word
        #Only take the first form of the first sense of a word
        elif "senses" in data.keys() and "tags" in data["senses"][0].keys():
            tags = data["senses"][0]["tags"]
            if "form-of" in tags and ("participle" in tags or "plural" in tags):
                stem = data["senses"][0]["form_of"][0]["word"].lower()
                if not stem.isalpha() or not stem.isascii(): continue
                word_to_stem, word_clusters = update_words(word_to_stem, word_clusters, word, stem)

    if SIMPLIFY_CLUSTERS:
        print("Simplifying clusters...", file=sys.stderr)
        word_to_stem, word_clusters = simplify_clusters(word_to_stem, word_clusters)

    return word_to_stem, word_clusters

def simplify_clusters(word_to_stem: Dict[str,str], word_clusters: Dict[str, Set[str]]):
    """
    Simplify all the chains of word -> stem -> superstem.
    """
    initial_stems = set(word_clusters.keys())
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
                word_clusters[super_stem].update(word_clusters[initial_stem])
                word_clusters.pop(initial_stem)
            except KeyError as e:
                problem_stems+=1
                traceback.print_exc()
                print(f"{e} => {initial_stem} -> {super_stem}")

    print(f"Total stems: {total_stems}\nTotal super stems: {total_super_stems}\nTotal problem stems: {problem_stems}")

    return word_to_stem, word_clusters

def print_word_to_stem(word_to_stem, filename):
    """
    Print the word -> stem pairs mappings to the given file.
    """
    sorted_words = sorted(set(word_to_stem.keys()))
    with open(filename, "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + " -> " + word_to_stem[word] + "\n")

def print_clusters(word_clusters, filename):
    """
    Print the stem -> word clusters to a file.

    Formatted as stem word1 word2 word3.....
    """
    with open(filename, "w", encoding="utf-8") as f:
        sorted_stems = sorted(set(word_clusters.keys()))
        for stem in sorted_stems:
            f.write(stem)
            for variant in word_clusters[stem]:
                f.write(" " + variant)
            f.write("\n")

def print_stems(word_clusters, filename):
    """
    Print a list of all the stems to a file.
    """
    sorted_stems = sorted(set(word_clusters.keys()))
    with open(filename, "w", encoding="utf-8") as f:
        for stem in sorted_stems:
            f.write(stem + "\n")

def print_words(word_to_stem, filename):
    """
    Print a list of all the words to a file.
    """
    sorted_words = sorted(set(word_to_stem.keys()))
    with open(filename, "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")

def main():
    wikt_data_en = list() #to hold all the raw data for English entries
    data: dict = None
    print("Reading Wiktionary data...", file=sys.stderr)
    if os.path.exists(WIKT_DATA_EN_FILE):
        with open(WIKT_DATA_EN_FILE, "rb") as f:
            wikt_data_en = pickle.load(f)
    else:
        with open(WIKT_DATA_RAW_FILE, "r") as f:
            for line in tqdm(f):
                data = json.loads(line)
                if "lang" in data.keys() and data["lang"] == "English":
                    wikt_data_en.append(data)
        with open(WIKT_DATA_EN_FILE, "wb") as f:
            pickle.dump(wikt_data_en, f)

    print("Processing Wiktionary words...", file=sys.stderr)
    word_to_stem, word_clusters = process_words(wikt_data_en)
    print(f"Total (word -> stem) pairs: {len(word_to_stem)}")

    if PRINT_WORD_TO_STEM:
        print("Writing word -> stem to file...", file=sys.stderr)
        print_word_to_stem(word_to_stem, "wordToStem.txt")
    if PRINT_CLUSTERS:
        print("Writing clusters to file...", file=sys.stderr)
        print_clusters(word_clusters, "clusters.txt")
    if PRINT_STEMS:
        print("Writing stems to file...", file=sys.stderr)
        print_stems(word_clusters, "stems.txt")
    if PRINT_WORDS:
        print("Writing words to file...", file=sys.stderr)
        print_words(word_to_stem, "words.txt")
    print("Complete!", file=sys.stderr)

if __name__ == "__main__":
    main()

