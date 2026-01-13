clueweb_path = "/home/harka424/Documents/COSC490/Stemming/Data/clueweb"
stemmers =  ["paiceHusk", "krovetz", "sStripping", "porter2", "lovins", "wikt"]
output_file = f"{clueweb_path}/stem_count.csv"

with open(output_file, "w") as f:
    f.write("stemmer,word,stem,count\n")

for stemmer in stemmers:
    stem_dict = dict()
    stem_map = dict()
    visited = set()
    current = ""
    input_file = f"{clueweb_path}/stems/{stemmer}.log"
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("Q:"):
                term = line[2:].split("->")
                stem_map[term[1].strip()] = term[0]
            if line.startswith("D:"):
                term = line[2:]
                term = term.split("->")
                stem = term[1].strip()
                if stem != current:
                    visited.add(current)
                    current = stem
                if stem in visited: 
                    continue
                if stem not in stem_dict:
                    stem_dict[stem] = 1
                else:
                    stem_dict[stem] += 1

    with open(output_file, "a") as f:
        for term in stem_dict:
            if term in stem_map:
                f.write(f"{stemmer},{stem_map[term]},{term},{stem_dict[term]}\n")
            else:
                f.write(f"{stemmer},{term},{term},{stem_dict[term]}\n")


            