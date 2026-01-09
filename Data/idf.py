clueweb_path = "/home/harka424/Documents/COSC490/Stemming/Data/clueweb"
stemmers =  ["paiceHusk", "krovetz", "sStripping", "porter2", "lovins", "wikt", "none"]
output_file = f"{clueweb_path}/idf.csv"

with open(output_file, "w") as f:
    f.write("stemmer,word,idf\n")

for stemmer in stemmers:
    idf_dict = dict()
    input_file = f"{clueweb_path}/idf/{stemmer}.log"
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("Q"):
                term = line[2:]
                term = term.split("->")
                idf_dict[term[0]] = term[1].strip()

    with open(output_file, "a") as f:
        for term in idf_dict:
            f.write(f"{stemmer},{term},{idf_dict[term]}\n")