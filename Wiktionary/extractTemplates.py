import json
import sys

target = sys.argv[1]

wiktionary_data = "raw-wiktextract-data.json"
words = list()  #list of all the English words in the Wiktionary
data: dict = None
print("Reading Wiktionary data...", file=sys.stderr)
with open(wiktionary_data, "r", encoding="utf-8") as f:
       for line in f:
           data = json.loads(line)
           if "lang" in data.keys() and data["lang"] == "English":
               if "word" not in data.keys(): continue
               print("Processing " + data["word"])
               if data["word"] == target:
                words.append(data)
target_file = target + ".txt"
with open(target_file, "w") as f:
     for word in words:
        print("--------------------------------------------------\n", file=f)
        for entry in word:
           print(entry, file=f)
           print(word[entry], file=f)
           print("\n", file=f)

# with open(wiktionary_data, "r", encoding="utf-8") as f:
#        for line in f:
#            data = json.loads(line)
#            if "lang" in data.keys() and data["lang"] == "English":
#                if "word" not in data.keys(): continue
#                print("Processing " + data["word"])
#                if "senses" not in data.keys(): continue
#                words.append(data)
# file = "multiple_forms_all.txt"
# with open(file, "w") as f:
#     for word in words:
#         skip = False
#         for sense in word["senses"]:
#              if "form_of" in sense.keys() and len(sense["form_of"]) > 1: break
#              skip = True
#              break
#         if skip: continue

                  
#         print("--------------------------------------------------\n", file=f)
#         for entry in word:
#             print(entry, file=f)
#             print(word[entry], file=f)
#             print("\n", file=f)
