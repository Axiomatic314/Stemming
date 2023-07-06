lookupTable = list()
with open("Wiktionary/replacements.txt", "r") as f:
    for line in f:
        contents = line.split(sep="->")
        lookupTable.append((contents[0].strip(), contents[1].strip()))

with open("Wiktionary/lookupTable.txt", "w") as f:
    f.write("{")
    for word, stem in lookupTable[:-1]:
        f.write("{\"" + word + "\",\"" + stem + "\"},\n")
    f.write("{\"" + lookupTable[-1][0] + "\",\"" + lookupTable[-1][0] + "\"}")
    f.write("}")
