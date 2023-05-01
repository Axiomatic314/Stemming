filename = "Stemmers/Snowball/snowballOutput.txt"
# filename = "Wiktionary/reducedReplacements.txt"
stem_clusters = dict()
stem_pairs = list()

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        contents = line.split(sep="->")
        stem_pairs.append((contents[0].strip(), contents[1].strip()))

for word, stem in stem_pairs:
    if stem not in stem_clusters.keys():
        stem_clusters[stem] = list()
    stem_clusters[stem].append(word)

for stem in stem_clusters:
    print(stem + ": ", end="")
    for word in stem_clusters[stem]:
        print(word, end=" ")
    print()
